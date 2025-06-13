import Jetson.GPIO as GPIO
from enum import Enum

class RobotState(Enum):
    # Name              = Pulse width (microseconds)
    BREATH_RED          = 1415    # Docked
    BREATH_SLOW         = 1545    # Idle
    LIGHT_CHASE_RED     = 1345    # To Pickup Station
    RED                 = 1885    # At Pickup Station
    CONFETTI            = 1065    # Item Picked Up
    LIGHT_CHASE_BLUE    = 1355    # To Delivery
    BLUE                = 1935    # At Delivery
    TWINKLES            = 1225    # Item Delivered
    LIGHT_CHASE_GRAY    = 1365    # Item Returning
    HEARTBEAT_SLOW      = 1515    # Charging
    STROBE_RED          = 1445    # Critical Error

class RobotStatusControl:
    def __init__(self, pin: int, numbering_mode = GPIO.BOARD, freq_hz: int = 50):
        GPIO.setmode(numbering_mode)
        self.pin = pin
        self.freq_hz = freq_hz
        self.pwm_object = None
        self._setup_pwm_pin()

    def _setup_pwm_pin(self):
        try:
            self.pwm_object = GPIO.PWM(self.pin, self.freq_hz)
            self.pwm_object.start(0)
            print(f"PWM set up on pin {self.pin} at {self.freq_hz} Hz.")
        except Exception as e:
            print(f"Error setting up PWM on pin {self.pin}: {e}. "
                  "Ensure pinmux is configured correctly and the pin is available for PWM.")
            self.pwm_object = None

    def set_robot_state_pattern(self, robot_state: RobotState):
        if not isinstance(robot_state, RobotState):
            print("Error: Invalid robot state provided. Must be a member of RobotState.")
            return
        
        if self.pwm_object is None:
            print(f"Error: PWM not initialised on pin {self.pin}. Cannot set robot state.")
            return
        
        pulse_width_us = robot_state.value
        period_us = 1_000_000 / self.freq_hz
        duty_cycle = (pulse_width_us / period_us) * 100

        try:
            self.pwm_object.ChangeDutyCycle(duty_cycle)
            print(f"Robot state pattern '{robot_state}' set on pin {self.pin}"
                  f" with {pulse_width_us}us pulse width ({duty_cycle:.2f}% duty cycle).")
        except Exception as e:
            print(f"Error changing duty cycle on pin {self.pin}: {e}")

    def _clear_robot_status_pattern(self):
        if self.pwm_object:
            try:
                self.pwm_object.stop()
                print(f"Robot status pattern cleared on pin {self.pin}.")
                self.pwm_object = None
            except Exception as e:
                print(f"Error stopping PWM on pin {self.pin} ")
        else:
            print("No robot status pattern is currently active on this pin.")

    def cleanup(self):
        self._clear_robot_status_pattern()