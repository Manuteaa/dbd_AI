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

    def find_skill_check(self, frame_grayscale, threshold=0.7):
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
    frame_test = cv2.imread(os.path.join("survivor", "skillCheckFinder", "frame.png"), cv2.IMREAD_GRAYSCALE)

    # Reshape to 1000x1000 (like in monitoring script)
    height, width = frame_test.shape[:2]
    crop_size = 1000
    center_y, center_x = height // 2, width // 2
    start_x = max(center_x - crop_size // 2, 0)
    start_y = max(center_y - crop_size // 2, 0)
    end_x = start_x + crop_size
    end_y = start_y + crop_size
    frame_test = frame_test[start_y:end_y, start_x:end_x]
    # cv2.imshow('frame', frame_test)
    # cv2.waitKey(0)

    skillCheckFinder = SkillCheckFinder()
    location = skillCheckFinder.find_skill_check(frame_test)
    print(location)

    if location is None:
        print("No skill check detected")
    else:
        top_left, bottom_right = location
        cv2.rectangle(frame_test, top_left, bottom_right, 255, 2)
        # cv2.imshow('skill check in frame', frame_test)
        # cv2.waitKey(0)

        skill_check = skillCheckFinder.crop_frame_from_location(frame_test, 224, top_left, bottom_right)
        # cv2.imshow('skill check 224x224', skill_check)
        # cv2.waitKey(0)
