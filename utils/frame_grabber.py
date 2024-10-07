import pyautogui


def get_monitor_attributes(object_size):
    width, height = pyautogui.size()
    monitor = {"top": height // 2 - object_size // 2,
               "left": width // 2 - object_size // 2,
               "width": object_size,
               "height": object_size}

    return monitor


def get_monitor_attributes_custom(top, left, w, h):
    width, height = pyautogui.size()

    if top <= 1.0:
        top = int(top * height)

    if left <= 1.0:
        left = int(left * width)

    if w <= 1.0:
        w = int(w * width)

    if h <= 1.0:
        h = int(h * height)

    monitor = {"top": top, "left": left, "width": w, "height": h}
    return monitor


def get_monitor_attributes_entire_screen():
    width, height = pyautogui.size()
    monitor = {"top": 0,
               "left": 0,
               "width": width,
               "height": height}

    return monitor
