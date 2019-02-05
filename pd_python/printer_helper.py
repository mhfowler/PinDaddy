import serial
uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)

import afruit_thermal_printer
ThermalPrinter = afruit_thermal_printer.get_printer_class(2.68)

printer = ThermalPrinter(uart)


def print_pin(number):
    printer.feed(1)
    printer.set_upside_down()
    encoded_number = '0000000000{}'.format(str(number))
    printer.print_barcode(encoded_number, printer.ITF)
    printer.print('Thank you for using Pin Daddy')
    printer.feed(10)


if __name__ == '__main__':
    print_pin(1234)