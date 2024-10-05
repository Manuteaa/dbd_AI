import cv2


class TemplateFinder:
    def __init__(self, template_filepath):
        self.template = cv2.imread(template_filepath, cv2.IMREAD_GRAYSCALE)

    def find_skill_check(self, frame_grayscale, threshold=0.4):
        res = cv2.matchTemplate(frame_grayscale, self.template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        # print(max_val)

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

    def crop_frame_from_location(self, frame, object_size, top_left, bottom_right):
        h, w = frame.shape[:2]
        center_x = (top_left[0] + bottom_right[0]) // 2  # col
        center_y = (top_left[1] + bottom_right[1]) // 2  # row
        demi_object_size = object_size // 2

        start_x = max(0, center_x - demi_object_size)
        start_y = max(0, center_y - demi_object_size)
        end_x = min(h, center_x + demi_object_size)
        # end_y = min(w, center_y + demi_object_size)
        end_y = start_y + 223

        padding_x = object_size - (end_x - start_x)
        padding_y = object_size - (end_y - start_y)
        padding_x_y = max(padding_x, padding_y)

        # To avoid seg-fault
        if padding_x_y != 0:
            frame = cv2.copyMakeBorder(frame, padding_x_y, padding_x_y, padding_x_y, padding_x_y, cv2.BORDER_REFLECT)

        crop = frame[start_y:end_y, start_x:end_x]
        return crop
