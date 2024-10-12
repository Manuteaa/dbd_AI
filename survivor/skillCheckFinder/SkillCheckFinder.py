import os
import cv2
import numpy as np

from utils.TemplateFinder import TemplateFinder


class SkillCheckFinder(TemplateFinder):
    def __init__(self):
        template_filepath = os.path.join("survivor", "skillCheckFinder", "template2.png")
        assert os.path.exists(template_filepath)
        super().__init__(template_filepath)

        # Resize template image & frame to optimize compute time in monitoring script
        self.ratio = 0.1
        self.template = self._resize(self.template)

    def _resize(self, image):
        new_size_x = int(image.shape[0] * self.ratio)
        new_size_y = int(image.shape[1] * self.ratio)
        return cv2.resize(image, dsize=(new_size_y, new_size_x), interpolation=cv2.INTER_AREA)

    def find_skill_check(self, frame_grayscale, threshold=0.8):
        frame_grayscale = self._resize(frame_grayscale)

        location = super().find_skill_check(frame_grayscale, threshold)
        if location is not None:
            center, score = location
            center = center / self.ratio
            center = np.floor(center).astype(int)
            return center, score
        else:
            return None


if __name__ == "__main__":
    from glob import glob
    from PIL import Image
    from tqdm import tqdm
    import random

    skillCheckFinder = SkillCheckFinder()
    images = glob(os.path.join("..", "dbd", "dataset", "*", "*.png"))
    random.shuffle(images)

    # from survivor.autoSkillCheck.AI_model import AI_model
    # ai = AI_model(onnx_filepath=os.path.join("..", "dbd", "model.onnx"))

    total_bin = np.full((12,), 0)
    errors_bin = np.full((12,), 0)
    with tqdm(total=len(images)) as pbar:
        for image in images:
            label = int(image.split(os.path.sep)[-2])
            total_bin[label] += 1

            frame = Image.open(image)
            frame_grayscale = skillCheckFinder.to_grayscale_array(np.asarray(frame))
            location = skillCheckFinder.find_skill_check(frame_grayscale)

            if (location is None and label != 0) or (location is not None and label == 0):
                errors_bin[label] += 1

            # frame = skillCheckFinder.crop_pil_frame_from_location(frame, 224, location[0])
            # frame = ai.pil_to_numpy(frame)
            # pred, desc, probs, should_hit = ai.predict(frame)
            # if pred != label:
            #     errors_bin[label] += 1

            pbar.set_description(str(errors_bin))
            pbar.update()

            # top_left, bottom_right = location
            # draw = ImageDraw.Draw(frame)
            # draw.rectangle((top_left[0], top_left[1], bottom_right[0], bottom_right[1]), outline="red", width=3)
            # frame.show()
            #
            # skill_check = skillCheckFinder.crop_pil_frame_from_location(frame, 224, top_left, bottom_right)
            # skill_check.show()
