from gamepad.Gamepad import Gamepad
import threading
import queue
import time

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO! This is probably because you need superuser privileges. You can achieve this by using sudo to run your script")


THROTTLE_FOWARD = 23
THROTTLE_BACKWARD = 18

STEERING_LEFT = 19
STEERING_RIGHT = 22

message_queue = queue.Queue()

def start_program():
    set_up_pins()
    pass

def set_up_pins():
    pins = [THROTTLE_FOWARD, STEERING_LEFT, THROTTLE_BACKWARD, STEERING_RIGHT]

    GPIO.setmode(GPIO.BCM)
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.setup(pin, GPIO.LOW)

def send_message(gamepad: Gamepad):
    message_queue.put(gamepad)
    print(gamepad)
    # Forward direction
    GPIO.output(THROTTLE_FOWARD, GPIO.HIGH)
    time.sleep(1000)
    GPIO.output(THROTTLE_FOWARD, GPIO.LOW)

