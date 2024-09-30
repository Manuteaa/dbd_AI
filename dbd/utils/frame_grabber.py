import pyautogui


def get_monitor_attributes():
    """Get monitor attributes for training
    Save entire main screen"""
    width, height = pyautogui.size()
    object_size = 1080
    monitor = {"top": height // 2 - object_size // 2,
               "left": width // 2 - object_size // 2,
               "width": object_size,
               "height": object_size}

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

    # width, height = pyautogui.size()
    # object_size = 224
    # monitor = {"top": height // 2 - object_size // 2,
    #            "left": width // 2 - object_size // 2,
    #            "width": object_size,
    #            "height": object_size}

    return monitor
