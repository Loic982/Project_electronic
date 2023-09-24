# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Basic `AHTx0` example test
"""

import time
import os
import board
import adafruit_ahtx0
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM) #type de fonction des GPIO 
GPIO.setwarnings(False) #desactive message d'alerte

# affectation broches GPIO

GPIO.setup(4, GPIO.OUT)

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_ahtx0.AHTx0(i2c)

GPIO.output(4, GPIO.LOW)
while True:
    print("\nTemperature: %0.1f C" % sensor.temperature)
    print("Humidity: %0.1f %%" % sensor.relative_humidity)
    if sensor.temperature > 28:
      GPIO.output(4, GPIO.HIGH)
    else:
      GPIO.output(4, GPIO.LOW)
    time.sleep(2)


