# DBD AI
An AI-based tool to help both survivors and killers in Dead by Daylight

Build upon my first project [dbd_autoSkillCheck](https://github.com/Manuteaa/dbd_autoSkillCheck), this repo aims to provide much more complete and advanced tools to help players to survive in dead by daylight.

We are in early phase of development, if you want to contribute, suggest features, or help us in any way, you can contact me on discord: manuteaa

## Features

### Survivor side
- **[Available]** Auto skill check AI : Automatic triggering of great skill checks through auto-pressing the space bar (fork of [dbd_autoSkillCheck](https://github.com/Manuteaa/dbd_autoSkillCheck))
- **[Available beta version]** Skill Check finder : An extension of Auto Skill Check to handle skill checks at random locations (such as doctor and Deadline skill checks)

### Killer side
- **[IN DEV]** Audio Helper AI : Give you visual clues of detected survivor's sounds and hatch
- **[IN DEV]** Hook Tracker : Track and display hook stages. Also displays a timer at unhooks to help you with some perks like decisive strike


## Execution Instructions

Create your own python env (I have python 3.11) and install the necessary libraries using the command :

`pip install numpy mss onnxruntime-gpu pyautogui IPython pillow gradio opencv-python`

Then git clone the repo.

### Survivor side

Run this script and play the game ! It will hit the space bar for you. For more details, see the [original repo](https://github.com/Manuteaa/dbd_autoSkillCheck)

`python run_monitoring_gradio.py`

### Killer side

There is no way you can make it work for now.
