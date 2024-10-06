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
            location = np.array(location) / self.ratio
            location = np.floor(location).astype(int)
            top_left, bottom_right = location[0], location[1]
            return top_left, bottom_right
        else:
            return None


if __name__ == "__main__":
    from PIL import Image, ImageDraw
    frame = Image.open(os.path.join("survivor", "skillCheckFinder", "frame.png"))

    # Reshape to 1000x1000 (like in monitoring script)
    height, width = frame.height, frame.width
    crop_size = 1000
    center_y, center_x = height // 2, width // 2
    start_x = max(center_x - crop_size // 2, 0)
    start_y = max(center_y - crop_size // 2, 0)
    end_x = start_x + crop_size
    end_y = start_y + crop_size
    frame = frame.crop((start_x, start_y, end_x, end_y))
    # frame.show()

    skillCheckFinder = SkillCheckFinder()
    frame_grayscale = skillCheckFinder.to_grayscale_array(np.asarray(frame))
    location = skillCheckFinder.find_skill_check(frame_grayscale)

    if location is None:
        print("No skill check detected")
    else:
        top_left, bottom_right = location
        draw = ImageDraw.Draw(frame)
        draw.rectangle((top_left[0], top_left[1], bottom_right[0], bottom_right[1]), outline="red", width=3)
        frame.show()

        skill_check = skillCheckFinder.crop_pil_frame_from_location(frame, 224, top_left, bottom_right)
        skill_check.show()
