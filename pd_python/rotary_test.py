from serial import Serial
import time
import threading
import random


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
        for rot in rots:
            GPIO.setup(rot, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        while True:
            # waiting for input
            print('++ waiting for input')

            for rot in rots:
                print('{}: {}'.format(rot, GPIO.input(rot)))
                time.sleep(2)

    finally:
        GPIO.cleanup()