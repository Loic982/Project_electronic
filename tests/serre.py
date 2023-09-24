import time
import board
import adafruit_ahtx0
import os
import RPi.GPIO as GPIO
import adafruit_mpu6050
import adafruit_ina260
import adafruit_ads1x15.ads1115 as ADS


from adafruit_ads1x15.analog_in import AnalogIn


i2c = board.I2C() #active les pins sda scl


GPIO.setmode(GPIO.BCM)  # type de fonction des GPIO
GPIO.setwarnings(False) # desactive les messages d'alerte


print("declaration du gyro accelero")
mpu = adafruit_mpu6050.MPU6050(i2c)  # declaration de l accelerometre
print("declaration aht20")
aht20 = adafruit_ahtx0.AHTx0(i2c)      # declaration aht20
print('declaration ina pompe')
inapompe = adafruit_ina260.INA260(i2c,address=65)
print('declaration ina verin')
inaverin = adafruit_ina260.INA260(i2c,address=64)
print('declaration ina panneau')
inapanneau  = adafruit_ina260.INA260(i2c,address=68)
print('declaration ina batterie')
inabatterie  = adafruit_ina260.INA260(i2c,address=69)
print('declaration ads1115')
ads =ADS.ADS1115(i2c)

# affectations des gpios utilisees

GPIO.setup(4, GPIO.OUT)   # gpio qui active la pompe
GPIO.setup(5, GPIO.OUT)   # gpio permettant de switcher le sens du verin
GPIO.setup(22, GPIO.OUT)  # gpio permettant de switcher le sens du verin
GPIO.setup(27, GPIO.OUT)  # gpio enalbe du ln298

# declaration des variables 

chan0 =AnalogIn(ads, ADS.P0)
chan1 =AnalogIn(ads, ADS.P1)
chan2 =AnalogIn(ads, ADS.P2)

humsol=chan0.vlaue   #valeur a échantilloner
soleil=chan1.value   #valeur a echantilloner
pluie =chan2.value   #valeur a echantilloner
tempint=aht20.temperature      #en celsius
humint=aht20.relative_humidity   #en pourcent
tempext=mpu.temperature       #en celsius
accel=mpu.acceleration     #en m par seconde carre
angle=mpu.gyro     #en radian par seconde



a=0

while True:
    print('debut de la boucle')
    time.sleep(2)
    print('affichage humidite sol')
    while a < 10:
      print(humsol)
      a += 1
      time.sleep(2)
    a=0
    print('affichage  soleil')
    while a<10:
        print(soleil)
        a+=1
        time.sleep(2)
    a=0
    print('affichage pluie')
    while a<10:
        print(pluie)
        a+=1
        time.sleep(2)
    a=0
    print('affichage temperature interieur')
    while a<10:
        print('\nTemperature: %0.1f c' %  tempint)
        a+=1
        time.sleep(2)
    a=0
    print('affichage l humidite interieur')
    while a<10:
        print("Humidity: %0.1f %%" % humint)
        a+=1
        time.sleep(2)
    a=0
    print('affichage temperature exterieur')
    while a<10:
        print("Temperature: %.2f C" % tempext)
        a+=1
        time.sleep(2)
    a=0
    print('affichage acceleration')
    while a<10:
        print(accel)
        a+=1
        time.sleep(2)
    a=0
    print('affichage gyroscope')
    while a<10:
        print(angle)
        a+=1
        time.sleep(2)
    a=0
    print('affichage inapompe')
    while a<10:
        print("Courant: %.2f mA Tension: %.2f V Puissance: %.2f mW" % (inapompe.current, inapompe.voltage, inapompe.power))
        a+=1
        time.sleep(2)
    a=0
    print('affichage inaverin')
    while a<10:
        print("Courant: %.2f mA Tension: %.2f V Puissance: %.2f mW" % (inaverin.current, inaverin.voltage, inaverin.power))
        a+=1
        time.sleep(2)
    a=0
    print('affichage inapanneau')
    while a<10:
        print("Courant: %.2f mA Tension: %.2f V Puissance: %.2f mW" % (inapanneau.current, inapanneau.voltage, inapanneau.power))
        a+=1
        time.sleep(2)
    a=0
    print('affichage inabatterie')
    while a<10:
        print("Courant: %.2f mA Tension: %.2f V Puissance: %.2f mW" % (inabatterie.current, inabatterie.voltage, inabatterie.power))
        a+=1
        time.sleep(2)
    a=0

