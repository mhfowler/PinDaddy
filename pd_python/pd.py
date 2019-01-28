import serial
import time

RPI = False

def click(s):
    pen_down(s)
    # then pen half up
    s.write(b'G90 G1 Z20 F3600\n')
    grbl_out = s.readline()

def pen_down(s):
    s.write(b'G90 G1 Z24 F3600\n')
    grbl_out = s.readline()

def pen_up(s):
    s.write(b'G90 G1 Z19 F3600\n')
    grbl_out = s.readline()

def home(s):
    pen_up(s)
    s.write(b'$H\n')
    grbl_out = s.readline()


def move(s, x=None, y=None):
    if x is not None and y is not None:
        s.write(b'G90 G1 X{x} Y{y} F3600\n'.format(x=x, y=y))
    elif x is not None:
        s.write(b'G90 G1 X{x} F3600\n'.format(x=x))
    elif y is not None:
        s.write(b'G90 G1 Y{y} F3600\n'.format(y=y))
    grbl_out = s.readline()


def block_phone():

    print '++ attempting to block phone'
    # change ACM number as found from ls /dev/tty/ACM*
    if RPI:
        s = serial.Serial("/dev/ttyUSB5", 115200)
    else:
        s = serial.Serial("/dev/tty.usbmodem14101", 115200)
    print '++ connected to serial'

    # Wake up grbl
    s.write("\r\n\r\n")
    time.sleep(2)  # Wait for grbl to initialize
    s.flushInput()  # Flush startup text in serial input

    # homing
    pen_up(s)
    home(s)
    pen_up(s)

    # then go
    move(s, x=20)
    move(s, y=35)
    click(s)
    move(s, y=45)
    move(s, x=23)
    click(s)

    # end with pen-down
    pen_down(s)

    # now go back home
    # home(s)
    s.close()
    print ('++ gcode sent')


# >>> ser.baudrate = 19200
# >>> ser.port = 'COM1'
# >>> ser.open()
# >>> ser.is_open
# True
# >>> ser.close()
# >>> ser.is_open
#
# def blink(pin):


if __name__ == '__main__':
    if RPI:
        try:
            import RPi.GPIO as GPIO

            btn = 23
            clk = 17
            dt = 18

            # setup button
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            # setup rotary encoder
            GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            counter = 0
            clkLastState = GPIO.input(clk)

            while True:
                # waiting for input
                print('++ waiting for input')

                # check rotary encoder
                clk_state = GPIO.input(clk)
                dt_state = GPIO.input(dt)
                print '++ clk_state: {}'.format(clk_state)
                print '++ dt_state: {}'.format(dt_state)
                if clk_state != clkLastState:
                    if dt_state != clk_state:
                        counter += 1
                    else:
                        counter -= 1
                print 'rotary_counter: {}'.format(counter)
                clkLastState = clk_state
                time.sleep(0.01)

                # check button
                input_state = GPIO.input(btn)
                if input_state == False:
                    print('++ button Pressed')
                    block_phone()
        finally:
            GPIO.cleanup()
    else:
        block_phone()