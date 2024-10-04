import os
import cv2

from utils.TemplateFinder import TemplateFinder


class SkillCheckFinder(TemplateFinder):
    def __init__(self):
        template_filepath = os.path.join("survivor", "skillCheckFinder", "template.png")
        assert os.path.exists(template_filepath)
        super().__init__(template_filepath)


if __name__ == "__main__":
    frame_test = cv2.imread(os.path.join("survivor", "skillCheckFinder", "test.png"), cv2.IMREAD_GRAYSCALE)

    skillCheckFinder = SkillCheckFinder()
    location = skillCheckFinder.find_skill_check(frame_test)

    if location is None:
        print("No skill check detected")
    else:
        top_left, bottom_right = location
        cv2.rectangle(frame_test, top_left, bottom_right, 255, 2)
        cv2.imshow('skill check in frame', frame_test)
        cv2.waitKey(0)

        center_x = (top_left[0] + bottom_right[0]) // 2  # col
        center_y = (top_left[1] + bottom_right[1]) // 2  # row
        skill_check = frame_test[center_y-112:center_y+112, center_x-112:center_x+112]  # TODO : assert no seg-fault
        cv2.imshow('skill check 224x224', skill_check)
        cv2.waitKey(0)
