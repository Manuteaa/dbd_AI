import os
import pathlib
import time

import gradio as gr
import numpy as np

from survivor.autoSkillCheck.AI_model import AI_model
from utils.directkeys import PressKey, ReleaseKey, SPACE


def monitor(onnx_ai_model, device, additional_features, debug_option):
    if onnx_ai_model is None or not os.path.exists(onnx_ai_model) or ".onnx" not in onnx_ai_model:
        raise gr.Error("Invalid onnx file", duration=0)

    if device is None:
        raise gr.Error("Invalid device option")

    if additional_features is None:
        raise gr.Error("Invalid additional_features option")

    if debug_option is None:
        raise gr.Error("Invalid debug option")

    # SkillCheckFinder feature
    skill_check_finder = None
    monitor = None
    if features[0] in additional_features:
        from survivor.skillCheckFinder.SkillCheckFinder import SkillCheckFinder
        skill_check_finder = SkillCheckFinder()

        from utils.frame_grabber import get_monitor_attributes
        monitor = get_monitor_attributes(800)

    # AI model
    use_gpu = (device == devices[1])
    ai_model = AI_model(onnx_ai_model, use_gpu, monitor=monitor)

    is_using_cuda = ai_model.is_using_cuda()
    if is_using_cuda:
        gr.Info("Running AI model on GPU (success)")
    else:
        gr.Info("Running AI model on CPU")
        if device == devices[1]:
            gr.Warning("Could not run AI model on GPU device. Check python console logs to debug.")

    # Variables
    t0 = time.time()
    nb_frames = 0
    nb_hits = 0

    # Create debug folders
    if debug_option == debug_options[2] or debug_option == debug_options[3]:
        pathlib.Path(debug_folder).mkdir(exist_ok=True)
        for folder_idx in range(len(ai_model.pred_dict)):
            pathlib.Path(os.path.join(debug_folder, str(folder_idx))).mkdir(exist_ok=True)

    while True:
        screenshot = ai_model.grab_screenshot()
        image_pil = ai_model.screenshot_to_pil(screenshot)
        nb_frames += 1

        if skill_check_finder is not None:
            # Skill Check detection from entire screen
            image_np = np.asarray(image_pil)
            image_np_grayscale = skill_check_finder.to_grayscale_array(image_np)
            location = skill_check_finder.find_skill_check(image_np_grayscale)
            if location is None:
                pred, desc, probs, should_hit = 0, "None", [], False
            else:
                top_left, bottom_right = location
                image_pil = skill_check_finder.crop_pil_frame_from_location(image_pil, 224, top_left, bottom_right)
                image_np = ai_model.pil_to_numpy(image_pil)
                pred, desc, probs, should_hit = ai_model.predict(image_np)

        else:
            # Standard 224x224 center crop
            image_np = ai_model.pil_to_numpy(image_pil)
            pred, desc, probs, should_hit = ai_model.predict(image_np)

        # Save all frames debug option
        if pred != 0 and debug_option == debug_options[3]:
            path = os.path.join(debug_folder, str(pred), "{}.png".format(nb_hits))
            image_pil.save(path)
            nb_hits += 1

        if should_hit:
            PressKey(SPACE)
            ReleaseKey(SPACE)

            yield gr.update(), image_pil, probs

            # Save hit skill checks debug option
            if debug_option == debug_options[2]:
                path = os.path.join(debug_folder, str(pred), "hit_{}.png".format(nb_hits))
                image_pil.save(path)
                nb_hits += 1

            time.sleep(0.5)
            t0 = time.time()
            nb_frames = 0
            continue

        # Compute fps
        t_diff = time.time() - t0
        if t_diff > 1.0:
            fps = round(nb_frames / t_diff, 1)

            if debug_option == debug_options[1]:
                yield fps, image_pil, gr.update()
            else:
                yield fps, gr.update(), gr.update()

            t0 = time.time()
            nb_frames = 0


if __name__ == "__main__":
    debug_folder = "saved_images"

    debug_options = ["None (default)",
                     "Display the monitored frame (a 224x224 center-cropped image, displayed at 1fps) instead of last hit skill check frame. Useful to check the monitored screen",
                     "Save hit skill check frames in {}".format(debug_folder),
                     "Save all skill check frames in {} (will impact fps)".format(debug_folder)]

    fps_info = "Number of frames per second the AI model analyses the monitored frame. Must be equal (or greater than) 60 to hit great skill checks properly. Check The GitHub FAQ for more details"
    devices = ["CPU (default)", "GPU"]
    onnx_path = os.path.join("survivor", "autoSkillCheck", "models", "model.onnx")
    features = ["Skill Check detection from entire screen"]

    demo = gr.Interface(title="DBD AI for survivors",
                        description="Please refer to https://github.com/Manuteaa/dbd_AI",
                        fn=monitor,
                        submit_btn="RUN",
                        clear_btn=None,

                        inputs=[gr.Dropdown(label="ONNX model filepath", choices=[onnx_path], value=onnx_path, info="Filepath of the ONNX model (trained AI model)"),
                                gr.Radio(choices=devices, value=devices[0], label="Device the AI onnx model will use"),
                                gr.CheckboxGroup(choices=features, label="Additional features", info="Additional features you want to enable. It may decrease AI model FPS."),
                                gr.Dropdown(label="Debug options", choices=debug_options, value=debug_options[0], info="Optional options for debugging or analytics"),
                                ],

                        outputs=[gr.Number(label="AI model FPS", info=fps_info),
                                 gr.Image(label="Last hit skill check frame", height=224),
                                 gr.Label(label="Skill check recognition")]
                        )
    demo.launch()


# if __name__ == "__main__":
#     import cProfile
#
#     debug_folder = "saved_images"
#     debug_options = ["None (default)",
#                      "Display the monitored frame (a 224x224 center-cropped image, displayed at 1fps) instead of last hit skill check frame. Useful to check the monitored screen",
#                      "Save hit skill check frames in {}".format(debug_folder),
#                      "Save all skill check frames in {} (will impact fps)".format(debug_folder)]
#
#     devices = ["CPU (default)", "GPU"]
#     onnx_path = os.path.join("survivor", "autoSkillCheck", "models", "model.onnx")
#     features = ["Skill Check detection from entire screen"]
#     onnx_path = os.path.join("survivor", "autoSkillCheck", "models", "model.onnx")
#
#     # monitor(onnx_path, devices[0], [features[0]], debug_options[0])
#     cProfile.run('monitor(onnx_path, devices[0], [features[0]], debug_options[0])', sort="time")
