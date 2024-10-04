import pyautogui


def get_monitor_attributes(object_size):
    width, height = pyautogui.size()
    monitor = {"top": height // 2 - object_size // 2,
               "left": width // 2 - object_size // 2,
               "width": object_size,
               "height": object_size}

    return monitor


def get_monitor_attributes_entire_screen():
    width, height = pyautogui.size()
    monitor = {"top": 0,
               "left": 0,
               "width": width,
               "height": height}

    return monitor
