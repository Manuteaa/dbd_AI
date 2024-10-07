import mss
import numpy as np
import os
from PIL import Image
from time import time

from utils.TemplateFinder import TemplateFinder
from utils.frame_grabber import get_monitor_attributes_custom


# TODO : track unhook stage ?
class HookTracker:
    def __init__(self):
        self.hook_templateFinder = TemplateFinder(os.path.join("killer", "HookTracker", "images", "hook.png"))

        self.players_hooks_count = [0] * 4
        self.players_are_hooked = [False] * 4
        self.players_unhooked_time = [0.] * 4

        self.mss = mss.mss()
        self.monitor = get_monitor_attributes_custom(0.38, 0.05, 0.03, 0.3)

    def grab_screenshot(self):
        screenshot = self.mss.grab(self.monitor)
        return screenshot

    def screenshot_to_pil(self, screenshot):
        return Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")

    def process_pil_frame(self, frame):
        frame = self.hook_templateFinder.to_grayscale_array(np.array(frame))
        height, width = frame.shape[:2]
        split_h = height // 4
        frames = [frame[i*split_h:(i+1)*split_h, :] for i in range(4)]
        return frames

    def predict_and_update(self, frames_grayscale):
        results = [self.hook_templateFinder.find_skill_check(sub_frame, 0.85) for sub_frame in frames_grayscale]

        for player_idx, result in enumerate(results):
            if result is None and self.players_are_hooked[player_idx]:
                # Player becomes unhooked
                self.players_are_hooked[player_idx] = False
                self.players_unhooked_time[player_idx] = time()  # start timer

            if result is not None and not self.players_are_hooked[player_idx]:
                # Player becomes hooked
                self.players_are_hooked[player_idx] = True
                self.players_unhooked_time[player_idx] = 0.  # reset timer
                self.players_hooks_count[player_idx] += 1

        return results

    def get_status(self):
        status = {}
        for player_idx in range(4):
            timer = self.players_unhooked_time[player_idx]  # time when unhooked
            if timer > 0:
                timer = int(time() - timer)  # elapsed time since unhook

                # Stop timer when elapsed time > 100s
                if timer > 100.:
                    timer = 0.

            status["player_{}".format(player_idx+1)] = {"hooked": str(self.players_are_hooked[player_idx]),
                                                        "hooks_count": self.players_hooks_count[player_idx],
                                                        "timer": timer}

        return status


if __name__ == "__main__":
    hook_tracker = HookTracker()
    screenshot = hook_tracker.grab_screenshot()
    pil_image = hook_tracker.screenshot_to_pil(screenshot)
    pil_image.show()

    hook_tracker.predict_and_update(np.array(pil_image))
