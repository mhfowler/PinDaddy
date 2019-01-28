import serial
uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)

import adafruit_thermal_printer
ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.68)

printer = ThermalPrinter(uart)

printer.test_page()