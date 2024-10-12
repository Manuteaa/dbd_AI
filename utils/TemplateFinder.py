import os.path

import cv2
import numpy as np
from PIL import ImageOps


class TemplateFinder:
    def __init__(self, template_filepath):
        assert os.path.exists(template_filepath)
        self.template = cv2.imread(template_filepath, cv2.IMREAD_GRAYSCALE)

    def find_skill_check(self, frame_grayscale, threshold=0.4):
        res = cv2.matchTemplate(frame_grayscale, self.template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        if max_val > threshold:
            h, w = self.template.shape
            top_left = max_loc
            center = np.array(top_left) + np.array([h, w]) // 2
            return center, round(max_val, 2)
        else:
            return None

    def to_grayscale_array(self, frame):
        frame_grayscale = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        return frame_grayscale

    def crop_pil_frame_from_location(self, frame, object_size, center):
        demi_object_size = object_size // 2
        demi_object_size = np.array([demi_object_size, demi_object_size])

        img_width, img_height = frame.size
        top_left = center - demi_object_size
        bottom_right = center + demi_object_size

        up, left = top_left
        bottom, right = bottom_right

        pad_up, pad_left, pad_bottom, pad_right = 0, 0, 0, 0
        if up < 0:
            pad_up = -up
            up = 0

        if left < 0:
            pad_left = -left
            left = 0

        if bottom > img_height:
            pad_bottom = bottom - img_height
            bottom = img_height

        if right > img_width:
            pad_right = right - img_width
            right = img_width

        crop = frame.crop((left, up, right, bottom))

        if pad_up != 0 or pad_left != 0 or pad_bottom != 0 or pad_right != 0:
            crop = ImageOps.expand(crop, (pad_left, pad_up, pad_right, pad_bottom))

        return crop

        # w, h = crop.size
        # if w != object_size or h != object_size:
        #     pad_left = (object_size - w) // 2
        #     pad_right = object_size - w - pad_left
        #
        #     pad_upper = (object_size - h) // 2
        #     pad_lower = object_size - h - pad_upper
        #
        #     crop = ImageOps.expand(crop, (pad_left, pad_upper, pad_right, pad_lower))
