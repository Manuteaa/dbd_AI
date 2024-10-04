import cv2
import numpy as np
from PIL import Image


class TemplateFinder:
    def __init__(self, template_filepath):
        self.template = cv2.imread(template_filepath, cv2.IMREAD_GRAYSCALE)

    def find_skill_check(self, frame_grayscale, threshold=0.4):
        res = cv2.matchTemplate(frame_grayscale, self.template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        if max_val > threshold:
            w, h = self.template.shape
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            return top_left, bottom_right
        else:
            return None

    def to_grayscale_array(self, frame):
        frame_grayscale = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        return frame_grayscale

    def crop_frame_from_location(self, frame, object_size, top_left, bottom_right):
        center_x = (top_left[0] + bottom_right[0]) // 2  # col
        center_y = (top_left[1] + bottom_right[1]) // 2  # row

        demi_object_size = object_size // 2
        crop = frame[center_y - demi_object_size:center_y + demi_object_size, center_x - demi_object_size:center_x + demi_object_size]
        return crop
