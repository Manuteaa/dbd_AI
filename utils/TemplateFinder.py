import cv2
import numpy as np
from PIL import ImageOps


class TemplateFinder:
    def __init__(self, template_filepath):
        self.template = cv2.imread(template_filepath, cv2.IMREAD_GRAYSCALE)

    def find_skill_check(self, frame_grayscale, threshold=0.4):
        res = cv2.matchTemplate(frame_grayscale, self.template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        print(max_val)

        if max_val > threshold:
            h, w = self.template.shape
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            return top_left, bottom_right
        else:
            return None

    def to_grayscale_array(self, frame):
        frame_grayscale = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        return frame_grayscale

    def crop_pil_frame_from_location(self, frame, object_size, top_left, bottom_right):
        center_x = (top_left[0] + bottom_right[0]) // 2  # col
        center_y = (top_left[1] + bottom_right[1]) // 2  # row
        demi_object_size = object_size // 2

        # frame = frame[:center_y+300, :center_x+50]
        # print(frame.shape)

        img_width, img_height = frame.size
        left = center_x - demi_object_size
        upper = center_y - demi_object_size
        right = center_x + demi_object_size
        lower = center_y + demi_object_size

        left = max(0, left)
        upper = max(0, upper)
        right = min(img_width, right)
        lower = min(img_height, lower)
        crop = frame.crop((left, upper, right, lower))

        w, h = crop.size
        if w != object_size or h != object_size:
            pad_left = (object_size - w) // 2
            pad_right = object_size - w - pad_left

            pad_upper = (object_size - h) // 2
            pad_lower = object_size - h - pad_upper

            crop = ImageOps.expand(crop, (pad_left, pad_upper, pad_right, pad_lower))

        return crop
