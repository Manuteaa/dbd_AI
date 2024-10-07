import cv2
import numpy as np
import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QFont, QColor, QPixmap
from pynput.keyboard import Key, Listener
from threading import Thread
import time
from PIL import ImageGrab
from datetime import datetime
from PyQt5.QtWidgets import QGraphicsOpacityEffect



def get_image_paths():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    pip_image_path = os.path.join(current_dir, "images/pip.png")
    hook_image_path = os.path.join(current_dir, "images/hook.png")

    return pip_image_path, hook_image_path


pip_image_path, hook_image_path = get_image_paths()

debug = False
# Detect screen resolution
screen_width, screen_height = ImageGrab.grab().size

# Original resolution ( 1920x1080)
original_width = 1920
original_height = 1080


# Fine-tuning factor for vertical positioning
def get_fine_tune_factor(screen_height):
    if screen_height < original_height:
        return 0.96  # manually tuned
    return 1.0  # No adjustment for 1920x1080


fine_tune_factor = get_fine_tune_factor(screen_height)

# Define original positions as percentages of the original resolution
overlay_positions_pct = [
    (200 / original_width, 410 / original_height),  # Overlay 1 position
    (200 / original_width, 480 / original_height),  # Overlay 2 position
    (200 / original_width, 580 / original_height),  # Overlay 3 position
    (200 / original_width, 670 / original_height),  # Overlay 4 position
]
# Convert original scanning area into relative percentages
x1_pct = 110 / original_width
y1_pct = 438 / original_height
x2_pct = 143 / original_width
y2_pct = 740 / original_height

# Dynamically calculate the scanning area based on current screen resolution
x1 = int(x1_pct * screen_width)
y1 = int(y1_pct * screen_height)
x2 = int(x2_pct * screen_width)
y2 = int(y2_pct * screen_height)

# Original region coordinates in percentages
regions_pct = [
    (438 / original_height, 475 / original_height),
    (527 / original_height, 564 / original_height),
    (615 / original_height, 652 / original_height),
    (702 / original_height, 739 / original_height),
]

# Calculate region coordinates dynamically
regions = [
    (int(start_pct * screen_height), int(end_pct * screen_height))
    for start_pct, end_pct in regions_pct
]


class KeySignal(QObject):
    keyPressed = pyqtSignal(int, int)
    imageMatched = pyqtSignal(int, int)


class TransparentOverlay(QWidget):
    instances = []
    active_states = [
        False,
        False,
        False,
        False,
    ]  # State tracking for image recognition activation
    startTimerSignal = pyqtSignal()
    resetTimerSignal = pyqtSignal()

    def __init__(self, position, size, initial_value=0):
        super().__init__()

        # Initialize the image labels list
        self.image_labels = []

        # Create a main layout to manage the positioning of the timer and images
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(-10, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Timer label setup
        self.timer_label = QLabel("80", self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(12)
        self.timer_label.setFont(font)
        self.timer_label.setStyleSheet("QLabel { color : blue; }")
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setOffset(1, 1)
        shadow_effect.setColor(QColor("black"))
        self.timer_label.setGraphicsEffect(shadow_effect)
        self.timer_label.setFixedSize(40, 30)

        # Opacity effect for timer label
        self.timer_opacity_effect = QGraphicsOpacityEffect()
        self.timer_label.setGraphicsEffect(self.timer_opacity_effect)
        self.timer_opacity_effect.setOpacity(0)  # Initially invisible

        self.main_layout.addWidget(self.timer_label)

        # Image layout to store image labels
        self.image_layout = QHBoxLayout()
        self.image_layout.setContentsMargins(0, 0, 0, 0)
        self.image_layout.setSpacing(0)
        self.main_layout.addLayout(self.image_layout)

        # Setup the geometry and window flags
        self.setGeometry(position[0] - 10, position[1], size[0] + 10, size[1])
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Timer setup
        self.timer = QTimer(self)
        self.timer.setInterval(1000)  # 1000 milliseconds
        self.timer.timeout.connect(self.update_timer)
        self.time_left = 80  # Initial time left for the timer

        # Connecting signals
        self.startTimerSignal.connect(self.start_timer)
        self.resetTimerSignal.connect(self.reset_timer)

        TransparentOverlay.instances.append(self)

    def create_image_label(self, pixmap):
        image_label = QLabel(self)
        image_label.setPixmap(pixmap)
        image_label.resize(5, 17)
        image_label.show()
        return image_label

    def update_images(self, count):
        """Dynamically update the number of images shown next to the counter."""
        for label in self.image_labels:
            self.image_layout.removeWidget(label)  # Remove it from the layout
            label.deleteLater()  # Delete the QLabel for cleanup
        self.image_labels.clear()  # Clear the list of image labels

        # Create and position new image labels based on the counter value
        for i in range(count):
            try:
                pixmap = QPixmap(pip_image_path)
                if pixmap.isNull():
                    raise FileNotFoundError(f"Image not found: {pip_image_path}")
            except Exception as e:
                print(f"Error loading image: {e}")
                return
            image_label = self.create_image_label(pixmap)
            self.image_labels.append(image_label)
            self.image_layout.addWidget(
                image_label
            )  # Add the image label to the image layout

    def set_timer_color(self):
        """Set the timer label color based on the remaining time."""
        if self.time_left == 80:
            self.timer_label.setStyleSheet("QLabel { color : blue; }")
        elif self.time_left == 70:
            self.timer_label.setStyleSheet("QLabel { color : green; }")
        elif self.time_left == 30:
            self.timer_label.setStyleSheet("QLabel { color : yellow; }")
        elif self.time_left <= 0:
            self.timer_label.setStyleSheet("QLabel { color : red; }")

    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(str(self.time_left))
        self.set_timer_color() 

        if self.time_left <= 0 or len(self.image_labels) == 3:
            self.timer.stop()
            self.timer_opacity_effect.setOpacity(0)

    def start_timer(self):
        if not self.timer.isActive():
            if len(self.image_labels) != 3:
                self.timer_opacity_effect.setOpacity(1)
                self.set_timer_color()  # Update the color based on the current time
                self.timer.start()

    def reset_timer(self):
        if len(self.image_labels) != 3:
            self.timer.stop()
            self.time_left = 80
            self.timer_label.setText(str(self.time_left))
            self.set_timer_color()  # Reset the color to match the reset time
            self.timer_opacity_effect.setOpacity(0)

    def updateValue(self, overlay_index, increment, from_keyboard=False):
        if overlay_index == TransparentOverlay.instances.index(self):
            current_value = len(
                self.image_labels
            )  # Base the value on the number of image labels
            new_value = current_value + increment

            # If the new value is 4 or greater, reset all counters
            if new_value >= 4:
                self.resetAllCounters()
            else:
                # Cap the value at 3 (since we only display up to 3 images)
                if new_value > 3:
                    new_value = 3
                # Call to update the number of images
                self.update_images(new_value)

            self.check_visibility_all()

    @classmethod
    def resetAllCounters(cls):
        for instance in cls.instances:
            instance.update_images(0)  # Reset images for each overlay
            instance.timer.stop()
            instance.timer_opacity_effect.setOpacity(0)
            instance.time_left = 80
            instance.timer_label.setText(str(instance.time_left))
        cls.active_states = [False, False, False, False]  # Reset active states
        cls.check_visibility_all()

    @classmethod
    def check_visibility_all(cls):
        # Check overall visibility based on all instances
        visible = any(len(instance.image_labels) > 0 for instance in cls.instances)
        for instance in cls.instances:
            instance.setVisible(visible)


def on_press(key):
    if hasattr(key, "char") and key.char in ("1", "2", "3", "4"):
        key_signal.keyPressed.emit(int(key.char) - 1, 1)


def scan_and_update():
    try:
        image_to_find = cv2.imread(hook_image_path, cv2.IMREAD_GRAYSCALE)
        if image_to_find is None:
            raise FileNotFoundError(f"Image not found: {hook_image_path}")
    except Exception as e:
        print(f"Error loading hook image: {e}")
        return

    previous_match_state = [False] * len(regions)

    while True:
        screen = np.array(ImageGrab.grab(bbox=(x1, y1, x2, y2)))
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        if debug:
            # Save the full scanned screen area for debugging
            save_debug_image(
                screen_gray,
                f"screen_area_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            )

        # Check if the scanning area is smaller than the template
        if (
            screen_gray.shape[0] < image_to_find.shape[0]
            or screen_gray.shape[1] < image_to_find.shape[1]
        ):
            # Resize the template to fit within the scanning area
            scaling_factor_height = screen_gray.shape[0] / image_to_find.shape[0]
            scaling_factor_width = screen_gray.shape[1] / image_to_find.shape[1]
            scaling_factor = min(scaling_factor_height, scaling_factor_width)

            # Resize the template image
            new_size = (
                int(image_to_find.shape[1] * scaling_factor),
                int(image_to_find.shape[0] * scaling_factor),
            )
            image_to_find_resized = cv2.resize(image_to_find, new_size)
            if debug:
                save_debug_image(
                    image_to_find_resized,
                    f"resized_template_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                )
        else:
            image_to_find_resized = image_to_find

        # Perform template matching with the resized template
        result = cv2.matchTemplate(
            screen_gray, image_to_find_resized, cv2.TM_CCOEFF_NORMED
        )

        for i, (start_y, end_y) in enumerate(regions):
            region_result = result[(start_y - y1) : (end_y - y1), :]

            # Get the maximum confidence value for this region
            _, region_max_val, _, _ = cv2.minMaxLoc(region_result)
            if debug:
                # Save each region from the original screen_gray for debugging
                region_debug = screen_gray[(start_y - y1) : (end_y - y1), :]
                timestamp = datetime.now().strftime("%H:%M:%S")

                # Save with confidence score and timestamp in the filename
                save_debug_image(
                    region_debug, f"region_{i+1}_{region_max_val:.2f}_{timestamp}.png"
                )

            overlay = TransparentOverlay.instances[i]
            if region_max_val > 0.55:
                if not TransparentOverlay.active_states[i]:
                    key_signal.imageMatched.emit(i, 1)  # Signal for a new match
                    TransparentOverlay.active_states[i] = True
                    overlay.resetTimerSignal.emit()  # Immediately reset timer since a match is found
                previous_match_state[i] = True
            else:
                if TransparentOverlay.active_states[i]:
                    TransparentOverlay.active_states[i] = False
                    overlay.startTimerSignal.emit()  # Emit signal to start timer only when match becomes non-match
                previous_match_state[i] = False

        time.sleep(3)


def save_debug_image(image, filename):
    debug_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "debug_images")
    if not os.path.exists(debug_dir):
        os.makedirs(debug_dir)

    # Handle grayscale and result matrices by normalizing them to save as images
    if len(image.shape) == 2:  # Grayscale or template matching result
        image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    filepath = os.path.join(debug_dir, filename)
    cv2.imwrite(filepath, image)
    print(f"Debug image saved: {filepath}")


def setup_overlays():
    # Use dynamically calculated positions
    overlays = [
        TransparentOverlay(overlay_positions[0], (20, 40), 0),  # Overlay 1
        TransparentOverlay(overlay_positions[1], (20, 40), 0),  # Overlay 2
        TransparentOverlay(overlay_positions[2], (20, 40), 0),  # Overlay 3
        TransparentOverlay(overlay_positions[3], (20, 40), 0),  # Overlay 4
    ]
    key_signal.keyPressed.connect(
        lambda idx, inc: overlays[idx].updateValue(idx, inc, from_keyboard=True)
    )
    key_signal.imageMatched.connect(
        lambda idx, inc: overlays[idx].updateValue(idx, inc, from_keyboard=False)
    )
    return overlays


def start_threads():
    listener_thread = Thread(target=lambda: Listener(on_press=on_press).start())
    listener_thread.daemon = True
    listener_thread.start()

    image_scan_thread = Thread(target=scan_and_update)
    image_scan_thread.daemon = True
    image_scan_thread.start()


if __name__ == "__main__":
    # Dynamically calculate overlay positions based on current resolution
    overlay_positions = [
        (int(x_pct * screen_width), int(y_pct * screen_height * fine_tune_factor))
        for x_pct, y_pct in overlay_positions_pct
    ]
    app = QApplication(sys.argv)
    key_signal = KeySignal()
    overlays = setup_overlays()
    start_threads()
    print("Monitoring...")
    sys.exit(app.exec_())
