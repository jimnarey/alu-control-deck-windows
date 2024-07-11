from typing import Type
from optparse import OptionParser, Values
from abc import ABC, abstractmethod
import time

import hid
import vgamepad as vg

import read
import shared

# ALU joystick input values
JOYSTICK_INDEX = 3
NEUTRAL = 8          # 00001000
UP = 128             # 10000000
DOWN = 68            # 01000100
LEFT = 22            # 00010110
RIGHT = 34           # 00100010
UP_LEFT = 150        # 10010110
UP_RIGHT = 162       # 10100010
DOWN_LEFT = 90       # 01011010
DOWN_RIGHT = 102     # 01100110

MAIN_BUTTON_INDEX = 0
A = 2
B = 4
X = 1
Y = 8
C = 128
Z = 32
SELECT = 64  # 1st controller device only

SECONDARY_BUTTON_INDEX = 1
START = 2
MENU = 16  # 1st controller device only


class Controller(ABC):

    def __init__(self, path, report_size):
        self.path = path
        self.report_size = report_size
        self.input = hid.device()
        self.input.open_path(self.path)
        self.joystick_value = 0
        self.main_buttons_value = 0
        self.secondary_buttons_value = 0

    def _poll(self):
        state = self.input.read(self.report_size)
        self.joystick_value = state[JOYSTICK_INDEX]
        self.main_buttons_value = state[MAIN_BUTTON_INDEX]
        self.secondary_buttons_value = state[SECONDARY_BUTTON_INDEX]

    @abstractmethod
    def set_output(self):
        raise NotImplementedError


class XboxGameController(Controller):

    def __init__(self, path, report_size):
        super().__init__(path, report_size)
        self.vpad = vg.VX360Gamepad()

    def set_output(self):

        self._poll()

        if self.joystick_value == NEUTRAL:
            print("neutral")
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
        elif self.joystick_value == UP:
            print("up")
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
            self.vpad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
        elif self.joystick_value == DOWN:
            print("down")
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
            self.vpad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
        elif self.joystick_value == LEFT:
            print("left")
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
            self.vpad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
        elif self.joystick_value == RIGHT:
            print("right")
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
            self.vpad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
        elif self.joystick_value == UP_LEFT:
            print("up_left")
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
            self.vpad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            self.vpad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
        elif self.joystick_value == UP_RIGHT:
            print("up_right")
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
            self.vpad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            self.vpad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
        elif self.joystick_value == DOWN_LEFT:
            print("down_left")
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
            self.vpad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            self.vpad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
        elif self.joystick_value == DOWN_RIGHT:
            print("down_right")
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
            self.vpad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
            self.vpad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)


        if self.main_buttons_value & A:
            self.vpad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        else:
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)

        if self.main_buttons_value & B:
            self.vpad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        else:
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)

        if self.main_buttons_value & X:
            self.vpad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
        else:
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)

        if self.main_buttons_value & Y:
            self.vpad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
        else:
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)

        if self.main_buttons_value & C:
            self.vpad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        else:
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)

        if self.main_buttons_value & Z:
            self.vpad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
        else:
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)

        if self.main_buttons_value & SELECT:
            self.vpad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
        else:
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)

        if self.secondary_buttons_value & START:
            self.vpad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
        else:
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)

        if self.secondary_buttons_value & MENU:
            self.vpad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE)
        else:
            self.vpad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE)

        self.vpad.update()


class DS4GameController(Controller):

    def __init__(self, path, report_size):
        super().__init__(path, report_size)
        self.vpad = vg.VDS4Gamepad()

    def set_output(self):

        self._poll()

        if self.joystick_value == NEUTRAL:
            self.vpad.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NONE)
        elif self.joystick_value == UP:
            self.vpad.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTH)
        elif self.joystick_value == DOWN:
            self.vpad.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTH)
        elif self.joystick_value == LEFT:
            self.vpad.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_WEST)
        elif self.joystick_value == RIGHT:
            self.vpad.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_EAST)
        elif self.joystick_value == UP_LEFT:
            self.vpad.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTHWEST)
        elif self.joystick_value == UP_RIGHT:
            self.vpad.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTHEAST)
        elif self.joystick_value == DOWN_LEFT:
            self.vpad.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTHWEST)
        elif self.joystick_value == DOWN_RIGHT:
            self.vpad.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_SOUTHEAST)

        
        if self.main_buttons_value & A:
            self.vpad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CROSS)
        else:
            self.vpad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CROSS)

        if self.main_buttons_value & B:
            self.vpad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE)
        else:
            self.vpad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE)

        if self.main_buttons_value & X:
            self.vpad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SQUARE)
        else:
            self.vpad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SQUARE)

        if self.main_buttons_value & Y:
            self.vpad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE)
        else:
            self.vpad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE)

        if self.main_buttons_value & C:
            self.vpad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT)
        else:
            self.vpad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT)

        if self.main_buttons_value & Z:
            self.vpad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT)
        else:
            self.vpad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT)

        if self.main_buttons_value & SELECT:
            self.vpad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SHARE)
        else:
            self.vpad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_SHARE)

        if self.secondary_buttons_value & START:
            self.vpad.press_button(button=vg.DS4_BUTTONS.DS4_BUTTON_OPTIONS)
        else:
            self.vpad.release_button(button=vg.DS4_BUTTONS.DS4_BUTTON_OPTIONS)

        if self.secondary_buttons_value & MENU:
            self.vpad.press_special_button(special_button=vg.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_PS)
        else:
            self.vpad.release_special_button(special_button=vg.DS4_SPECIAL_BUTTONS.DS4_SPECIAL_BUTTON_PS)

        self.vpad.update()


def get_controllers(device_specs: list[dict], config: dict[str, dict], v_class: Type[Controller]) -> list[Controller]:
    controllers = []
    for device_spec in device_specs:
        if f"{device_spec.get("vendor_id")}:{device_spec.get("product_id")}" in config["devices"]:
            if device_spec.get("usage_page") == 1 and device_spec.get("usage") == 5:
                controllers.append(v_class(device_spec["path"], config["report_size"]))
    return controllers


def get_virtual_controller_class(options: Values) -> Type[Controller]:
    if options.type.lower() == "ds4":
        return DS4GameController
    return XboxGameController


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-r", "--read", dest="read", action="store_true", default=False)
    parser.add_option("-t", "--type", dest="type", default="360")
    (options, args) = parser.parse_args()
    if options.read:
        read.read_all_devices()
    else:
        v_class = get_virtual_controller_class(options)
        device_specs = hid.enumerate()
        config = shared.get_config()
        controllers = get_controllers(device_specs, config, v_class)
        controllers = [controllers[0]]
        while True:
            for controller in controllers:
                controller.set_output()
            time.sleep(0.002)



