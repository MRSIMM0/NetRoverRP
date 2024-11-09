from gamepad.Gamepad import Gamepad
import threading
import queue
import time

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO! This is probably because you need superuser privileges. You can achieve this by using sudo to run your script")


THROTTLE_FORWARD = 23
THROTTLE_BACKWARD = 18

STEERING_LEFT = 19
STEERING_RIGHT = 22

def start_program():
    set_up_pins()
    pass

def set_up_pins():
    pins = [THROTTLE_FORWARD, STEERING_LEFT, THROTTLE_BACKWARD, STEERING_RIGHT]

    GPIO.setmode(GPIO.BCM)
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
    GPIO.output(THROTTLE_FORWARD, GPIO.LOW)
    GPIO.output(THROTTLE_BACKWARD, GPIO.LOW)

    GPIO.output(STEERING_LEFT, GPIO.HIGH)
    GPIO.output(STEERING_RIGHT, GPIO.HIGH)

def receive_message(gamepad: Gamepad):
    x ,y = gamepad.LEFT_STICK.axis
    if x > 0.8:
        GPIO.output(STEERING_RIGHT, GPIO.LOW)
        GPIO.output(STEERING_LEFT, GPIO.HIGH)
    elif x < -0.8:
        GPIO.output(STEERING_LEFT, GPIO.LOW)
        GPIO.output(STEERING_RIGHT, GPIO.HIGH)
    else:
        GPIO.output(STEERING_LEFT, GPIO.HIGH)
        GPIO.output(STEERING_RIGHT, GPIO.HIGH)

