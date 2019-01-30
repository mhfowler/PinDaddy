from serial import Serial
import time
import threading
import random
import RPi.GPIO as GPIO

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
    rd = {}
    set_of_true_vals = set([])
    for rot in rots:
        val = GPIO.input(rot)
        rd[rot] = val
        if val:
            set_of_true_vals.add(rot)

    # print('true_vals: {}'.format(set_of_true_vals))

    set1 = {5, 6, 12, 16, 19, 21, 26}
    set2 = {5, 6, 12, 19, 20, 21, 26}
    set3 = {5, 6, 12, 16, 19, 20, 21}
    set4 = {5, 12, 16, 19, 20, 21, 26}
    set5 = {5, 6, 16, 19, 20, 21, 26}
    set6 = {5, 6, 12, 16, 19, 20, 26}
    if set1 == set_of_true_vals:
        return 1
    elif set2 == set_of_true_vals:
        return 2
    elif set3 == set_of_true_vals:
        return 3
    elif set4 == set_of_true_vals:
        return 4
    elif set5 == set_of_true_vals:
        return 5
    elif set6 == set_of_true_vals:
        return 6
    else:
        print('++ unexpected rotary value')
        return 0

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
            print('++ rot_val: {}'.format(rot_val))
            time.sleep(2)

    finally:
        GPIO.cleanup()