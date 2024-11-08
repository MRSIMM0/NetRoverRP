from gamepad.Gamepad import Gamepad
import threading
import queue

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

STEERING_PWM_PIN = 18
THROTTLE_PWM_PIN = 19

STEERING_DIRECTION_PIN = 22
THROTTLE_DIRECTION_PIN = 23

message_queue = queue.Queue()

def start_program():
    set_up_pins()
    threading.Thread(target=loop, args=(message_queue,)).start()
    pass

def set_up_pins():
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(STEERING_PWM_PIN, GPIO.OUT)
    GPIO.setup(THROTTLE_PWM_PIN, GPIO.OUT)
    GPIO.setup(STEERING_DIRECTION_PIN, GPIO.OUT)
    GPIO.setup(THROTTLE_DIRECTION_PIN, GPIO.OUT)

def loop(queue):
    while True:
        if(queue.empty()):
            continue
        gamepad = queue.get()

        print(gamepad.LEFT_STICK)
        print(gamepad.RIGHT_STICK)
        print(gamepad.LEFT_TRIGGER)
        print(gamepad.RIGHT_TRIGGER)


def send_message(gamepad: Gamepad):
    message_queue.put(gamepad)
    pass

