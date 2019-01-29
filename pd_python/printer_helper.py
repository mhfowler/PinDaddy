import serial
uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)

import afruit_thermal_printer
ThermalPrinter = afruit_thermal_printer.get_printer_class(2.68)

printer = ThermalPrinter(uart)


def print_pin(number):
    printer.print('Thank you using Pin Daddy')
    printer.feed(2)
    encoded_number = '00000000{}'.format(str(number))
    printer.print_barcode(encoded_number, printer.ITF)
    printer.feed(2)


if __name__ == '__main__':
    print_pin(1234)