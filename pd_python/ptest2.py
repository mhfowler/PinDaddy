import serial
uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)

import afruit_thermal_printer
ThermalPrinter = afruit_thermal_printer.get_printer_class(2.68)

printer = ThermalPrinter(uart)


def print_number(number):
    printer.print('Thank you using Pin Daddy')
    printer.feed(2)

    printer.print_barcode(str(number), printer.UTC_A)
    printer.feed(2)


if __name__ == '__main__':
    print_number(123456789012)