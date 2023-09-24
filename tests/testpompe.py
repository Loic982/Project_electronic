import time
import os
import board
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM) #type de fonction des GPIO
GPIO.setwarnings(False) #desactive message d'alerte

# affectation broches GPIO

GPIO.setup(4, GPIO.OUT)

GPIO.output(4, GPIO.LOW)


while True:
    print("Pompe active")
    GPIO.output(4, GPIO.HIGH)
    time.sleep(5)
    print("Pompe desactive")
    GPIO.output(4, GPIO.LOW)
    time.sleep(5)

