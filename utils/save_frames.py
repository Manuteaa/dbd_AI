import pathlib
import mss
import time
import os

from PIL import Image

from utils.frame_grabber import get_monitor_attributes


if __name__ == '__main__':
    # Make new dataset folder, where we save the frames
    pathlib.Path("dataset").mkdir(exist_ok=True)
    timestr = time.strftime("%Y%m%d-%H%M%S")
    dataset_folder = os.path.join("dataset", timestr)
    pathlib.Path(dataset_folder).mkdir(exist_ok=True)

    # Get monitor attributes
    monitor = get_monitor_attributes()

    with mss.mss() as sct:
        print("Saving images in {}".format(dataset_folder))
        i = 0

        # Infinite loop
        while True:
            screenshot = sct.grab(monitor)
            image_pil = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            image_pil = image_pil.resize((380, 380), resample=Image.LANCZOS)
            image_pil.save(os.path.join(dataset_folder, "{}_{}.png".format(timestr, i)))
            i += 1
