# DBD Hook Stage Counter & Protection Time Tracker

The **Dead by Daylight DBD Hook Stage Counter & Protection Time Tracker** is a Python tool that helps killers remember each survivor's hook stage and track the remaining time for their basekit Borrowed Time, Decisive Strike, and Off the Record perks. It is built using PyQt5 for the graphical interface and OpenCV for image processing.

![demo](images/demo.gif "demo")

<!-- TOC -->
* [Features](#features)
* [Roadmap](#roadmap)
* [Installation](#installation)
* [Project Details](#project-details)
* [FAQ](#faq)
* [Known Issues](#known-issues)
<!-- TOC -->

## Features
- Tracks survivor hook stages.
- Displays timers for Borrowed Time, Decisive Strike, and Off the Record perks.
- Automatically updates the overlay based on image recognition (when the hook icon is detected).
- Real-time, non-intrusive overlays.
- **TODO:** Automatically add +1 to a stage counter if the survivor is not unhooked on time or if they kill themselves.

## Installation

1. **Download and Install Python:**
   - Make sure Python is installed on your system. I tested it on Python 3.12.3. You can download it from the [official Python website](https://www.python.org/).

2. **Clone the Repository:**
   - `git clone https://github.com/Manuteaa/dbd_AI`

3. **Navigate to the project directory:**

4. **Install dependencies:**

   - `pip install -r requirements.txt`

## Project Details

### On-Screen Overlay Display:
The application creates small, semi-transparent windows (overlays) on your screen that show counters and images. These overlays can display information such as the time remaining or how many times you have hooked a specific survivor. 

### Keyboard Interaction:
You can manually increment the counter using your keyboard. For example, pressing keys `1`, `2`, `3`, or `4` will add to the respective counters. This is useful when a survivor progresses to the next hook stage after being hooked once. To reset the counter for the next match, simply set any of the counters to '4'.

### Image Recognition:
When a hook icon appears on the screen, the application automatically recognizes it and updates the counter accordingly.

### Timers:
Each counter has an associated timer. When the application detects that a survivor is no longer hooked, the timer starts counting down. 
- The timer changes color to indicate how much time is left:
  **Blue:** Basekit Borrowed Time is active.
  **Green:** Decisive Strike is active.
  **Yellow:** Off the Record is active.

## FAQ

### Why does the script do nothing?
- Check if there are any errors in the Python console logs.
- Ensure that your game settings (UI scale, filters) are configured correctly, as non-standard settings might interfere with image recognition.

### What about the anti-cheat system?
- Although the script does not modify or interact directly with game files, it is impossible to guarantee that it will never be flagged by an anti-cheat system. Use the application at your own risk.

## Known Issues

### Screen Resolution Limitations:
- The application is designed to work with a 16:9 aspect ratio and a standard UI scale. It has been primarily tested on a 1920x1080 resolution but should function on any 16:9 resolution. If you are using a different aspect ratio, the application will not work correctly.

### In-Game Filters:
- If you use in-game filters (such as contrast, brightness, or color filters), these visual changes may interfere with the image recognition, making it harder for the application to detect the hook image. If you encounter issues, try disabling filters or replacing the default hook image (located in the `/images` folder) with one that suits your setup.


