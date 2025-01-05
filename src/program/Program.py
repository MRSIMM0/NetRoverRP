from gamepad.Gamepad import Gamepad
import threading
import queue
import time

# RPi.GPIO is used to control the GPIO pins on a Raspberry Pi.
# If run on a non-RPi environment, this import may fail unless mocked or replaced.
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!")

# Define the GPIO pin numbers (BCM numbering) for throttle and steering
THROTTLE_FORWARD = 18
THROTTLE_BACKWARD = 23
STEERING_LEFT = 19
STEERING_RIGHT = 22

def start_program():
    """
    Entry point to set up the GPIO pins before handling gamepad events.
    """
    set_up_pins()
    pass  # Placeholder - no additional code here currently

def set_up_pins():
    """
    Configure each of the required GPIO pins as output and set initial states.
    """
    # List of pins that we'll be using for controlling throttle and steering
    pins = [THROTTLE_FORWARD, STEERING_LEFT, THROTTLE_BACKWARD, STEERING_RIGHT]

    # Use BCM GPIO numbering
    GPIO.setmode(GPIO.BCM)
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)

    # Initialize throttle pins to LOW (no power)
    GPIO.output(THROTTLE_FORWARD, GPIO.LOW)
    GPIO.output(THROTTLE_BACKWARD, GPIO.LOW)

    # Initialize steering pins to HIGH (neutral state)
    GPIO.output(STEERING_LEFT, GPIO.HIGH)
    GPIO.output(STEERING_RIGHT, GPIO.HIGH)

def receive_message(gamepad: Gamepad):
    """
    Main function to handle incoming gamepad inputs.
    Calls the relevant handling functions for steering and throttle.
    """
    handle_steering(gamepad)
    handle_throttle(gamepad)

def handle_steering(gamepad: Gamepad):
    """
    Reads the LEFT_STICK axis from the gamepad and sets steering GPIO pins accordingly.
    If the stick is moved left/right beyond a threshold, engage one steering direction.
    Otherwise, default to a neutral steering mode.
    """
    x, y = gamepad.LEFT_STICK.axis  # x and y components of the left stick

    # If x < -0.8, steer sharply to the left
    if x < -0.8:
        GPIO.output(STEERING_RIGHT, GPIO.LOW)
        GPIO.output(STEERING_LEFT, GPIO.HIGH)
    # If x > 0.8, steer sharply to the right
    elif x > 0.8:
        GPIO.output(STEERING_LEFT, GPIO.LOW)
        GPIO.output(STEERING_RIGHT, GPIO.HIGH)
    # Otherwise, set both steering pins to HIGH (neutral position)
    else:
        GPIO.output(STEERING_LEFT, GPIO.HIGH)
        GPIO.output(STEERING_RIGHT, GPIO.HIGH)

def handle_throttle(gamepad: Gamepad):
    """
    Controls forward/backward throttle and braking based on trigger and A button inputs:
      - RIGHT_TRIGGER => forward
      - LEFT_TRIGGER => backward
      - A_BUTTON     => brake
    """
    foward = gamepad.RIGHT_TRIGGER.pressed  # True if right trigger is pressed
    backward = gamepad.LEFT_TRIGGER.pressed # True if left trigger is pressed
    brake = gamepad.A_BUTTON.pressed        # True if A button is pressed

    # If the A button (brake) is pressed, engage both forward and backward simultaneously
    if brake:
        GPIO.output(THROTTLE_FORWARD, GPIO.HIGH)
        GPIO.output(THROTTLE_BACKWARD, GPIO.HIGH)
    # If forward trigger is pressed, set forward pin HIGH, backward pin LOW
    elif foward:
        GPIO.output(THROTTLE_FORWARD, GPIO.HIGH)
        GPIO.output(THROTTLE_BACKWARD, GPIO.LOW)
    # If backward trigger is pressed, set backward pin HIGH, forward pin LOW
    elif backward:
        GPIO.output(THROTTLE_FORWARD, GPIO.LOW)
        GPIO.output(THROTTLE_BACKWARD, GPIO.HIGH)
    # Otherwise, turn both throttle outputs LOW (idle)
    else:
        GPIO.output(THROTTLE_FORWARD, GPIO.LOW)
        GPIO.output(THROTTLE_BACKWARD, GPIO.LOW)
