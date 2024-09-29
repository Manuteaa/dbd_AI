import pyautogui


def get_monitor_attributes():
    """Get monitor attributes for training
    Save entire main screen"""
    width, height = pyautogui.size()
    monitor = {"top": 0,
               "left": 0,
               "width": width,
               "height": height}

    return monitor


def get_monitor_attributes_test():
    """ Get monitor attributes for inference
    Save entire main screen
    """
    width, height = pyautogui.size()
    monitor = {"top": 0,
               "left": 0,
               "width": width,
               "height": height}

    return monitor
