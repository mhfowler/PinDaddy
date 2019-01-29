from serial import Serial
import time
import threading
import random

rot5 = 5
rot6 = 6
rot13 = 13
rot19 = 19
rot26 = 26
rot12 = 12
rot16 = 16
rot20 = 20
rot21 = 21
rots = [
    rot5, rot6, rot13, rot19, rot26, rot12, rot16, rot20, rot21
]


def get_rot_value():
    rot_dict = {}
    for rot in rots:
        val = GPIO.input(rot)
        print('{}: {}'.format(rot, val))
        rot_dict[rot] = val






if __name__ == '__main__':
    import RPi.GPIO as GPIO

    try:

        clk = 17
        dt = 18
        btn = 23

        # setup button
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # setup rots
        for rot in rots:
            GPIO.setup(rot, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        while True:
            # waiting for input
            print('++ waiting for input')
            rot_val = get_rot_value()
            time.sleep(2)

    finally:
        GPIO.cleanup()