import serial
import time

def click(s):
    s.write(b'G90 G1 Z24 F3600\n')
    grbl_out = s.readline()
    s.write(b'G90 G1 Z20 F3600\n')
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

    # change ACM number as found from ls /dev/tty/ACM*
    s = serial.Serial("/dev/tty.usbmodem14101", 115200)

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

    # now go back home
    home(s)
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
    block_phone()