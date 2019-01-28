import serial
import time
import threading

RPI = True

# Define your callback
def rt_callback(scale_position):
    print('Hello world! The scale position is {}'.format(scale_position))

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
        import RPi.GPIO as GPIO
        from pyky040 import pyky040
        try:

            clk = 17
            dt = 18
            btn = 23

            # setup button
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            # Init the encoder pins
            my_encoder = pyky040.Encoder(CLK=17, DT=18, SW=27)

            # Setup the options and callbacks (see documentation)
            my_encoder.setup(scale_min=0, scale_max=100, step=2, loop=True, chg_callback=rt_callback)

            # Launch the listener
            my_thread = threading.Thread(target=my_encoder.watch)

            # Launch the thread
            my_thread.start()
            print '++ rotary encoder initialized'

            while True:
                # waiting for input
                print('++ waiting for input')

                # check button
                input_state = GPIO.input(btn)
                if input_state == False:
                    print('++ button Pressed')
                    block_phone()
        finally:
            GPIO.cleanup()
    else:
        block_phone()