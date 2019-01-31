from serial import Serial
import time
import threading
import random


RPI = True
if RPI:
    from pd_python.rotary_test import get_rot_value, rots

phones = {
    1: 'iphone 6',
    2: 'iphone 5',
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

    def get_calibration(self):
        phone_calibrations = {
            'iphone 6': {
                'column1x': -15.5,
                'row1y': 36.5,
                'column2x': -21.5,
                'row2y': 39,
                'column3x': -28,
                'row3y': 42
            },
            'iphone 5': {
                'column1x': -16,
                'row1y': 34,
                'column2x': -21,
                'row2y': 37,
                'column3x': -26,
                'row3y': 39.5
            }
        }
        if self.phone not in phone_calibrations:
            print('++ not yet implemented')
            return None
        else:
            return phone_calibrations[self.phone]

    def press_number(self, num):
        calibration = self.get_calibration()
        if num == 1:
            col = 1
            row = 1
            x_pos = calibration['column1x']
            y_pos = calibration['row1y']
        elif num == 2:
            col = 2
            row = 1
            x_pos = calibration['column2x']
            y_pos = calibration['row1y']
        elif num == 3:
            col = 3
            row = 1
            x_pos = calibration['column3x']
            y_pos = calibration['row1y']
        elif num == 4:
            col = 1
            row = 2
            x_pos = calibration['column1x']
            y_pos = calibration['row2y']
        elif num == 5:
            col = 2
            row = 2
            x_pos = calibration['column2x']
            y_pos = calibration['row2y']
        elif num == 6:
            col = 3
            row = 2
            x_pos = calibration['column3x']
            y_pos = calibration['row2y']
        elif num == 7:
            col = 1
            row = 3
            x_pos = calibration['column1x']
            y_pos = calibration['row3y']
        elif num == 8:
            col = 2
            row = 3
            x_pos = calibration['column2x']
            y_pos = calibration['row3y']
        elif num == 9:
            col = 3
            row = 3
            x_pos = calibration['column3x']
            y_pos = calibration['row3y']
        else:
            raise Exception('Invalid number')
        # move and click
        self.move(x_pos, y_pos)
        self.pen_down(row=row)
        self.pen_up()

    def write(self, msg):
        self.serial.write(msg.encode())

    def pen_down(self, row=None):
        z = 21.5
        if row == 3:
            z = 21.5
        self.write('G90 G1 Z{} F3600\n'.format(z))
        grbl_out = self.serial.readline()

    def pen_up(self):
        self.write('G90 G1 Z19 F3600\n')
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

    def enter_pin(self, pin):
        # first pen  up
        self.pen_up()

        # then click each digit
        for digit in pin:
            self.press_number(int(digit))

    def block_phone(self):

        if RPI:
            rot_value = get_rot_value()
        else:
            rot_value = 1
        self.phone = phones[rot_value]
        print('++ attempting to block phone: {}', self.phone)

        # first select random pin
        pin = ''
        for i in range(4):
            digit = random.randint(1, 9)
            pin += str(digit)
        print('++ printing pin: {}'.format(pin))

        # first print the pin
        self.print_pin(pin)

        # first pen  up
        self.pen_up()

        # then click each digit
        self.enter_pin(pin)
        self.enter_pin(pin)

        # now go back home
        print('++ returning home')
        self.pen_up()
        self.move(x=-2, y=2)
        time.sleep(1)

        # ideally home the device again
        self.home()
        self.pen_up()


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

            # setup rots
            for rot in rots:
                GPIO.setup(rot, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            print('++ beginning to wait for input')
            while True:

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