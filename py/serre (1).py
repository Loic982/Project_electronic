import time
import board
import adafruit_ahtx0
import os
import RPi.GPIO as GPIO
import adafruit_mpu6050
import adafruit_ina260
import adafruit_ads1x15.ads1115 as ADS
import mysql.connector
import datetime
import adafruit_dht
import psutil

from adafruit_ads1x15.analog_in import AnalogIn


i2c = board.I2C() #active les pins sda scl


GPIO.setmode(GPIO.BCM)  # type de fonction des GPIO
GPIO.setwarnings(False) # desactive les messages d'alerte

for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()
        
sensor = adafruit_dht.DHT11(board.D18)

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

# affectations des gpios utilisés
gpio_pompe = 27
gpio_verin_1 = 24 #ouverture
gpio_verin_2 = 25 #fermeture
gpio_verin_enable = 26
print('declaration GPIO')
GPIO.setup(gpio_pompe, GPIO.OUT)   # gpio qui active la pompe
GPIO.setup(gpio_verin_1, GPIO.OUT)   # gpio permettant de switcher le sens du verin
GPIO.setup(gpio_verin_2, GPIO.OUT)  # gpio permettant de switcher le sens du verin
GPIO.setup(gpio_verin_enable, GPIO.OUT)  # gpio enalbe du ln298


GPIO.output(gpio_verin_enable, GPIO.LOW)
GPIO.output(gpio_verin_2, GPIO.LOW)
GPIO.output(gpio_verin_1, GPIO.LOW)
GPIO.output(gpio_pompe, GPIO.LOW)
# declaration des variables 
print('declaration chan')
chan0 =AnalogIn(ads, ADS.P0)
chan1 =AnalogIn(ads, ADS.P1)
chan2 =AnalogIn(ads, ADS.P2)

humsol=chan0.value   #valeur à échantilloner
soleil=chan2.value   #valeur à echantilloner
pluie =chan1.value   #valeur à echantilloner
tempint=aht20.temperature      #en celsius
humint=aht20.relative_humidity   #en pourcent
tempext=mpu.temperature       #en celsius
accel=mpu.acceleration     #en m par seconde au carré




fenetre_ouvert = False  #boucle affichage 10 fois
print("Début boucle")

while True:
   print("temperature et humidite interne")
   while a < 10:
      temp = sensor.temperature
      humidity = sensor.humidity
      print("Temperature: {}*C   Humidity: {}% ".format(temp, humidity))
      a += 1
      time.sleep(1)
   a=0
    db_connector = mysql.connector.connect(
        host="localhost",
        user="groupe3",
        password="groupe3",
        database="groupe3_db"
    )
    
    db_cursor = db_connector.cursor()

    #humidité sol
    humid_sol = chan0.value
    
    #humidité air
    humid_air = aht20.relative_humidity

    #affichage  soleil
    light=chan2.value

    #affichage pluie
    rain_rate = chan1.value
    rain = False
    
    #affichage température intérieure
    print('affichage temperature interieur')
    while a<10:
        print('\nTemperature: %0.1f c' %  tempint)
        a+=1
        time.sleep(1)
    a=0
    #affichage humidité intérieure
    print('affichage l humidite interieur')
    while a<10:
        print("Humidity: %0.1f %%" % humint)
        a+=1
        time.sleep(1)
    a=0
    temp_int = aht20.temperature
    
    #temperature extérieure

    temp_ext = mpu.temperature

    #acceleration
    accel = mpu.acceleration
    accel_array = list(i for i in accel)
    angle = ((accel_array[0]-1.5)/0.2)+15
    angle_mini = 20
    angle_maxi = 40

    #pompe
    i_pompe = inapompe.current
    v_pompe = inapompe.voltage
    p_pompe = inapompe.power
    
    #verin
    i_verin = inaverin.current
    v_verin = inaverin.voltage
    p_verin = inaverin.power
    
    #panneau solaire
    i_sp = inapanneau.current
    v_sp = inapanneau.voltage
    p_sp = inapanneau.power
    
    #batterie
    i_batt = inabatterie.current
    v_batt = inabatterie.voltage
    p_batt = inabatterie.power
    
    #moment
    moment = datetime.datetime.now()
    print("Début connexion")
    request = ('INSERT INTO sensor_data (humid_air, humid_sol, temp_int, temp_ext, angle, light, rain, i_pompe, v_pompe, p_pompe, i_verin, v_verin, p_verin, i_batt, v_batt, p_batt, i_sp, v_sp, p_sp, moment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
    values = (humid_air, humid_sol, temp_int, temp_ext, angle, light, rain, i_pompe, v_pompe, p_pompe, i_verin, v_verin, p_verin, i_batt, v_batt, p_batt, i_sp, v_sp, p_sp, moment)
    db_cursor.execute(request, values)
    db_connector.commit()
    print("Fin connexion")
    time.sleep(5)
    
    #control
    db_cursor.execute('SELECT * FROM status')
    
    status_tuple = db_cursor.fetchall()
    status = list(i for i in status_tuple)
    
    if status[0]==True:
        #Partie automatique
        if humid_sol<60: #Activation pompe si humidité du sol inférieur à 60
            GPIO.output(gpio_pompe, GPIO.HIGH)
            db_cursor.execute('UPDATE status SET pompe_on=true')
        elif humid_sol>85:#Désactivation pompe si humidité du sol supérieur à 85
            GPIO.output(gpio_pompe, GPIO.LOW)
            db_cursor.execute('UPDATE status SET pompe_on=false')
        
        if temp_int>30 & temp_int>temp_ext & fenetre_ouvert==False:
            #Ouverture fenêtre si la température intérieur est supérieur à 30 degrés
            # et si la température intérieur est supérieur à la température extérieur 
            #et que la fenêtre n'est pas déjà ouverte
            GPIO.output(gpio_verin_2, GPIO.LOW)
            accel = mpu.acceleration
            accel_array = list(i for i in accel)
            angle = ((accel_array[0]-1.5)/0.2)+15
            while angle<40:
                accel = mpu.acceleration
                accel_array = list(i for i in accel)
                angle = ((accel_array[0]-1.5)/0.2)+15
                GPIO.output(gpio_verin_1, GPIO.HIGH)
                if angle>=40:
                    GPIO.output(gpio_verin_2, GPIO.LOW)
                    GPIO.output(gpio_verin_1, GPIO.LOW)
            #Mise à jour de la BD
            db_cursor.execute('UPDATE status SET fenetre_ouvert=true')
            
        elif temp_int<18 & temp_int<temp_ext & fenetre_ouvert==True:
            #Fermeture fenêtre si la température intérieur est inférieur à 18 degrés
            # et si la température intérieur est inférieur à la température extérieur 
            #et que la fenêtre n'est pas déjà fermée
            GPIO.output(gpio_verin_1, GPIO.LOW)
            accel = mpu.acceleration
            accel_array = list(i for i in accel)
            angle = ((accel_array[0]-1.5)/0.2)+15
            while angle>20:
                accel = mpu.acceleration
                accel_array = list(i for i in accel)
                angle = ((accel_array[0]-1.5)/0.2)+15
                GPIO.output(gpio_verin_2, GPIO.HIGH)
                if angle>=20:
                    GPIO.output(gpio_verin_2, GPIO.LOW)
                    GPIO.output(gpio_verin_1, GPIO.LOW)
             #Mise à jour de la BD
            db_cursor.execute('UPDATE status SET fenetre_ouvert=false')
        else
            GPIO.output(gpio_verin_enable, GPIO.LOW)
            GPIO.output(gpio_verin_2, GPIO.LOW)
            GPIO.output(gpio_verin_1, GPIO.LOW)

    elif status[0]==False:
        #Partie manuelle
        #Activation ou désactivation de la pompe 
        if status[1]==True:
           GPIO.output(gpio_pompe, GPIO.HIGH)
                       db_cursor.execute('UPDATE status SET pompe_on=true')
        elif status[1]==False:
            GPIO.output(gpio_pompe, GPIO.LOW)
            db_cursor.execute('UPDATE status SET pompe_on=false')
        
        #Gestion de l'activation manuelle du vérin
        if status[2]!=fenetre_ouvert:
            if fenetre_ouvert==True:
                #Si la fenêtre est déjà ouverte, on la ferme
            GPIO.output(gpio_verin_1, GPIO.LOW)
            accel = mpu.acceleration
            accel_array = list(i for i in accel)
            angle = ((accel_array[0]-1.5)/0.2)+15
            while angle>20:
                accel = mpu.acceleration
                accel_array = list(i for i in accel)
                angle = ((accel_array[0]-1.5)/0.2)+15
                GPIO.output(gpio_verin_2, GPIO.HIGH)
                if angle>=20:
                    GPIO.output(gpio_verin_2, GPIO.LOW)
                    GPIO.output(gpio_verin_1, GPIO.LOW)
                #Mise à jour de la BD
                db_cursor.execute('UPDATE status SET fenetre_ouvert=false')
            elif fenetre_ouvert==False:
                #Si la fenêtre est fermée, on l'ouvre
            GPIO.output(gpio_verin_2, GPIO.LOW)
            accel = mpu.acceleration
            accel_array = list(i for i in accel)
            angle = ((accel_array[0]-1.5)/0.2)+15
            while angle<40:
                accel = mpu.acceleration
                accel_array = list(i for i in accel)
                angle = ((accel_array[0]-1.5)/0.2)+15
                GPIO.output(gpio_verin_1, GPIO.HIGH)
                if angle>=40:
                    GPIO.output(gpio_verin_2, GPIO.LOW)
                    GPIO.output(gpio_verin_1, GPIO.LOW)
                #Mise à jour de la BD
                db_cursor.execute('UPDATE status SET fenetre_ouvert=false')
