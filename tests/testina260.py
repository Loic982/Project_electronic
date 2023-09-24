
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_ina260
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


i2c = board.I2C()
ina260 = adafruit_ina260.INA260(i2c,address=65)



GPIO.setup(4, GPIO.OUT)


while True:
    print(ina260)
    print(
        "Current: %.2f mA Voltage: %.2f V Power:%.2f mW"
        % (ina260.current, ina260.voltage, ina260.power)
    )
    time.sleep(1)
    GPIO.output(4, GPIO.HIGH)   
    time.sleep(1)
    print(
        "Current: %.2f mA Voltage: %.2f V Power:%.2f mW"
        % (ina260.current, ina260.voltage, ina260.power)
    )
    time.sleep(1)
    GPIO.output(4, GPIO.LOW)
    time.sleep(1)
