import os
import cv2


class SkillCheckFinder:
    def __init__(self):
        current_folder = os.path.dirname(os.path.abspath(__file__))
        self.template = cv2.imread(os.path.join(current_folder, "template.png"), cv2.IMREAD_GRAYSCALE)
        # self.template = self.template[70:220, 90:230]

    def find_skill_check(self, frame_grayscale, threshold=0.4):
        # convert frame to grayscale
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # RGB ?

        # Template matching
        res = cv2.matchTemplate(frame_grayscale, self.template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        print(max_val)

        if max_val > threshold:
            w, h = self.template.shape
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            return top_left, bottom_right
        else:
            return None


if __name__ == "__main__":
    frame_test = cv2.imread("test.png", cv2.IMREAD_GRAYSCALE)

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
