import time

import gradio as gr

from killer.HookTracker.HookTracker import HookTracker


def monitor(additional_features, debug_option):
    if additional_features is None:
        raise gr.Error("Invalid additional_features option")

    if debug_option is None:
        raise gr.Error("Invalid debug option")

    # Ai model
    ai_model = HookTracker()

    # Variables
    t0_fps = time.time()
    nb_frames = 0

    while True:
        screenshot = ai_model.grab_screenshot()
        image_pil = ai_model.screenshot_to_pil(screenshot)
        frames = ai_model.process_pil_frame(image_pil)
        nb_frames += 1

        # Run status analysis
        results = ai_model.predict_and_update(frames)
        status = ai_model.get_status()

        # Update fps
        t_diff = time.time() - t0_fps
        if t_diff > 0.2:
            fps = round(nb_frames / t_diff, 1)

            if debug_option == debug_options[1]:
                # update fps, status and displayed frames
                yield (fps,
                       frames[0], status["player_1"]["hooks_count"], status["player_1"]["timer"],
                       frames[1], status["player_2"]["hooks_count"], status["player_2"]["timer"],
                       frames[2], status["player_3"]["hooks_count"], status["player_3"]["timer"],
                       frames[3], status["player_4"]["hooks_count"], status["player_4"]["timer"]
                       )
            else:
                # update fps and status
                yield (fps,
                       gr.update(), status["player_1"]["hooks_count"], status["player_1"]["timer"],
                       gr.update(), status["player_2"]["hooks_count"], status["player_2"]["timer"],
                       gr.update(), status["player_3"]["hooks_count"], status["player_3"]["timer"],
                       gr.update(), status["player_4"]["hooks_count"], status["player_4"]["timer"]
                       )

            t0_fps = time.time()
            nb_frames = 0


if __name__ == "__main__":
    fps_info = "Number of frames per second the AI model analyses the monitored frame"
    debug_options = ["None", "Display the monitored frames"]
    features = []

    with gr.Blocks(title="DBD AI for killers") as demo:
        with gr.Row(equal_height=False):
            with gr.Column(variant="panel"):
                additional_features = gr.CheckboxGroup(choices=features, label="Additional features", info="Additional features you want to enable. It may decrease AI FPS.")
                debug_option = gr.Dropdown(label="Debug options", choices=debug_options, value=debug_options[1], info="Optional options for debugging or analytics", interactive=True)
                # run = gr.Button("RUN", variant="primary", visible=True)
                run = gr.Button("RUN (NIN CURRENT DEV)", variant="primary", visible=True, interactive=False)

            with gr.Column(variant="panel"):
                with gr.Row():
                    fps = gr.Number(label="AI FPS", info=fps_info, interactive=False)

                with gr.Row():
                    frame1 = gr.Image(label="Player 1 status", height=100, width=200, interactive=False, scale=2)
                    hook_count1 = gr.Number(label="Hooks stage", interactive=False)
                    timer1 = gr.Number(label="Timer", interactive=False)

                with gr.Row():
                    frame2 = gr.Image(label="Player 2 status", height=100, width=200, interactive=False, scale=2)
                    hook_count2 = gr.Number(label="Hooks stage", interactive=False)
                    timer2 = gr.Number(label="Timer", interactive=False)

                with gr.Row():
                    frame3 = gr.Image(label="Player 3 status", height=100, width=200, interactive=False, scale=2)
                    hook_count3 = gr.Number(label="Hooks stage", interactive=False)
                    timer3 = gr.Number(label="Timer", interactive=False)

                with gr.Row():
                    frame4 = gr.Image(label="Player 4 status", height=100, width=200, interactive=False, scale=2)
                    hook_count4 = gr.Number(label="Hooks stage", interactive=False)
                    timer4 = gr.Number(label="Timer", interactive=False)

        run.click(monitor, inputs=[additional_features, debug_option], outputs=[fps, frame1, hook_count1, timer1, frame2, hook_count2, timer2, frame3, hook_count3, timer3, frame4, hook_count4, timer4])

    demo.launch()

