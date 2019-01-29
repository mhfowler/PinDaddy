from serial import Serial
import time
import threading
import random
from pd_python.rotary_test import get_rot_value


RPI = True
if RPI:
    from pyky040 import pyky040

phones = {
    1: 'iphone 6',
    2: 'iphone 7',
    3: 'iphone 7+',
    4: 'samsung galaxy'
}


class PD:
    def __init__(self):
        self.selected_phone = 'iphone 6'

        # initialize grbl and home
        # change ACM number as found from ls /dev/tty/ACM*
        if RPI:
            self.serial = Serial("/dev/ttyACM0", 115200)
        else:
            self.serial = Serial("/dev/tty.usbmodem14101", 115200)
        print('++ connected to serial')

        # Wake up grbl
        self.write('\r\n\r\n')
        time.sleep(2)  # Wait for grbl to initialize
        self.serial.flushInput()  # Flush startup text in serial input
        print('++ grbl initialized')

        #  unlock
        self.write('$X\n')

        # then home
        self.home()

    def print_pin(self, pin):
        if RPI:
            from pd_python import printer_helper
            print('++ printing pin: {}'.format(pin))
            printer_helper.print_pin(str(pin))
        else:
            print('++ pin: {}'.format(pin))

    def write(self, msg):
        self.serial.write(msg.encode())

    def click(self):
        self.pen_down()
        # then pen half up
        self.write('G90 G1 Z22 F3600\n')

    def pen_down(self):
        self.write('G90 G1 Z26 F3600\n')
        grbl_out = self.serial.readline()

    def pen_up(self):
        self.write('G90 G1 Z20 F3600\n')
        grbl_out = self.serial.readline()

    def home(self):
        print('++ homing')
        self.write('$H\n')
        grbl_out = self.serial.readline()

    def move(self, x=None, y=None):
        if x is not None and y is not None:
            self.write('G90 G1 X{x} Y{y} F3600\n'.format(x=x, y=y))
        elif x is not None:
            self.write('G90 G1 X{x} F3600\n'.format(x=x))
        elif y is not None:
            self.write('G90 G1 Y{y} F3600\n'.format(y=y))
        grbl_out = self.serial.readline()

    def block_phone(self):

        if RPI:
            rot_value = get_rot_value()
        else:
            rot_value = 1
        self.phone = phones[rot_value]
        print('++ attempting to block phone: {}', self.phone)

        # first select random pin
        pin = random.randint(0, 9999)

        # then print pin
        self.print_pin(pin)

        # pen up
        self.pen_up()

        # then go
        self.move(x=-20)
        self.move(y=35)
        self.click()
        self.move(y=45)
        self.move(x=-23)
        self.click()

        # now go back home
        time.sleep(2)
        print('++ returning home')
        self.home()
        print('++ gcode sent')


if __name__ == '__main__':
    pd = PD()
    if RPI:
        import RPi.GPIO as GPIO

        try:

            clk = 17
            dt = 18
            btn = 23

            # setup button
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            while True:
                # waiting for input
                print('++ waiting for input')

                # check button
                input_state = GPIO.input(btn)
                if input_state == False:
                    print('++ button Pressed')
                    pd.block_phone()
                else:
                    time.sleep(0.1)
        finally:
            GPIO.cleanup()
    else:
        pd.block_phone()