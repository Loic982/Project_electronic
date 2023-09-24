

import time
import os
import board
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM) #type de fonction des GPIO
GPIO.setwarnings(False) #desactive message d'alerte

# affectation broches GPIO

GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)

GPIO.output(27, GPIO.LOW)
GPIO.output(22, GPIO.LOW)
GPIO.output(5, GPIO.LOW)

GPIO.output(27, GPIO.HIGH)
while True:
    GPIO.output(27, GPIO.HIGH)
    print("INPUT 1 active")
    GPIO.output(5, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(5, GPIO.LOW)
    time.sleep(1)
    print("INPUT 2 active")
    GPIO.output(22, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(22, GPIO.LOW)
    time.sleep(1)
    print("sortie desactivée")
    GPIO.output(27, GPIO.LOW)
    time.sleep(5)


