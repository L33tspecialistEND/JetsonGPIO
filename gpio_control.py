import Jetson.GPIO as GPIO
from enum import Enum

class GPIOControl:
    class NumberingMode(Enum):
        BOARD = GPIO.BOARD
        BCM = GPIO.BCM
        CVM = GPIO.CVM
        TEGRA = GPIO.TEGRA_SOC
    
    class Direction(Enum):
        IN = GPIO.IN
        OUT = GPIO.OUT

    def __init__(self, mode = NumberingMode.BOARD):
        GPIO.setmode(mode.value)
        self.mode = mode
        self.pin_states = {}
        self.pin_directions = {}
        self.pwm_objects = {}
        self.current_robot_state_pin = None

    def cleanup(self):
        GPIO.cleanup()

    def print_num_mode(self):
        if self.mode == self.NumberingMode.BCM:
            print("BCM numbering mode set.")
        elif self.mode == self.NumberingMode.CVM:
            print("CVM numbering mode set.")
        elif self.mode == self.NumberingMode.TEGRA:
            print("TEGRA_SOC numbering mode set.")
        else:
            print("BOARD numbering mode set.")

    def setup_pin(self, pin, direction, initial = GPIO.LOW):
        if pin in self.pin_directions:
            print(f"Warning: Pin {pin} is already configured.")
            return

        GPIO.setup(pin, direction.value)
        self.pin_directions[pin] = direction

        if direction == self.Direction.OUT:
            GPIO.output(pin, initial)
            self.pin_states[pin] = bool(initial)

    def _validate_output_pin(self, pin):
        if pin not in self.pin_directions:
            print(f"Warning: Pin {pin} has not been configured.")
            return
        if self.pin_directions[pin] == self.Direction.IN:
            print(f"Warning: Pin {pin} has been configured as an input pin.")
            return
        return True
    
    def set_high(self, pin):
        if not self._validate_output_pin(pin):
            return
        GPIO.output(pin, GPIO.HIGH)
        self.pin_states[pin] = True

    def set_low(self, pin):
        if not self._validate_output_pin(pin):
            return
        GPIO.output(pin, GPIO.LOW)
        self.pin_states[pin] = False

    def toggle(self, pin):
        if not self._validate_output_pin(pin):
            return
        if self.pin_states[pin] == False:
            self.set_high(pin)
        else:
            self.set_low(pin)

    def read_pin_state(self, pin):
        if pin not in self.pin_directions:
            print(f"Error: Pin {pin} has not been configured.")
            return False

        if self.pin_directions[pin] == self.Direction.IN:
            return GPIO.input(pin)

        return self.pin_states.get(pin, False)

    def pin_function(self, pin):
        if pin not in self.pin_directions:
            print(f"Error: Pin {pin} has not been configured.")
            return

        direction = self.pin_directions[pin]
        print(f"Pin {pin} is an {'input' if direction == self.Direction.IN else 'output'} pin.")