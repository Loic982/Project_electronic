# Projet 3BSI_Connected GreenHouse
# Groupe 2
# PITOT Maxime - SMAÏN JADDOUK - OMARI Nabil
""" Description:
Control of a connected greenhouse
INPUT:
- Air Humidity [0]
- Ground Humidity [1]
- Inside Temperature [2]
- Outside Temperature [3]
- Window orientation [4]
- Pump Current [5]
- Pump Voltage [6]
- Pump Power [7]
- Cylinder Current [8]
- Cylinder Voltage [9]
- Cylinder Power [10]
- Battery Current [11]
- Battery Voltage [12]
- Battery Power [13]
- Solar Panel Current [14]
- Solar Panel Voltage [15]
- Solar Panel Power [16]
- Rain [17]
- Luminosity [18]
- Date and Time [19]

OUTPUT:
- Mode [0]
- Pump [1]
- Cylinder [2]

CONTROL:
- error detection system 
- passive temperature regulation with the opening/closing of the window
- ground humidity regulation with the control of the pump

IMPROVMENT:
- Physical UI 
=> INPUT = Automatic/Manual switch + pump ON/OFF switch + Cylinder UP/DOWN buttons
=> OUPTUT = red LED for actuator activation + green LED for system status
=> FUNCTIONALITIES = send an email with the error code if an error occur
"""
    
import secrets
import RPi.GPIO as GPIO
import smbus
import board
import adafruit_ina260
import adafruit_ahtx0
import adafruit_mpu6050
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import mysql.connector
import time
import math
from pathlib import Path
from datetime import datetime

#Define PIN
cyl_pwm1 = 18 #IN1
cyl_pwm2 = 22 #IN2
cyl_en = 37 #EN
pump = 13 #relay

#Define variable
#scaling
tilt_min = 0                #min window angle
tilt_max = 90               #max window angle
temp_threshold_min = 12     #temperature threshold to open the window
temp_threshold_max = 25     #temperature threshold to close the window
hum_ground_min = 55         #humidity threshold to activate the pump
hum_ground_max = 85         #humidity threshold to desactivate the pump
rain_min = 25000               #min rain to declare the raining flag
cyl_min = 200               #min power consumption of the cylinder
cyl_max = 2000              #max power consumption of the cylinder
pump_min = 200              #min power consumption of the pump
pump_max = 2000             #max power consumption of the pump
bat_min = 20                #min power consumption of the battery
bat_max = 2000              #max power consumption of the battery
delay = 5001                #sampling delay

connection = 0              #parameter to connect to the DB          
task = 0                    #task requested (writing/reading)

#val
db_val = []                 #array with the values of the interface (auto/manu switch, ON/OFF switch, up/down buttons)
data_list = []              #array with the measured values
error = []                  #array with the errors detected during the process
actual_time = 0             #current date and time
mode = 0                    #mode: 0 = auto, 1 = manual
stop = False
groupe = "groupe2"
pswd = "groupe2"
database_name = "groupe2_db"
status = "starting..."

#Sensor register
adc = ADS.ADS1115(board.I2C(0x68))              #Adress analog to digital converter
lum = AnalogIn(adc,ADS.P0)                      #Adress luminosity sensor
rain = AnalogIn(adc, ADS.P1)                    #Adress rain sensor 
hum_ground = AnalogIn(adc, ADS.P2)              #Adress ground humidity sensor
Tins = adafruit_ahtx0.AHTx0(board.I2C())        #Adress AHT20 sensor (humidity air + t°air inside)
Tout = adafruit_mpu6050.MPU6050(board.I2C())    #Adress MPU6050 (accelerometer + t°air outside)
bat = adafruit_ina260.INA260(board.I2C(69))     #Adress INA260 battery
solar = adafruit_ina260.INA260(board.I2C(68))   #Adress INA260 solar panel
pump = adafruit_ina260.INA260(board.I2C(65))    #Adress INA260 pump
cyl = adafruit_ina260.INA260(board.I2C(64))     #Adress INA260 cylinder

def main():
    status = "main running"
    
    Startup()                               #Program initialisation (pinout, database connection)
    
    while(stop == False):           
        start = time.time()                 #Start chrono
        
        mode_test()                         #Interface data sampling (reading)
        
        if delay <= 0 | delay > 5000:       
            measure()                       #Data sampling (sampling + writing)
            delay = 5000
        
        output()                            #Pump & Cylinder control
        
        end = time.time()                   #Stop chrono
        delay = delay - (end-start)*1000    #Update Sampling period
        
def Startup():
    #boot of the system, clear data, initialization of the variables, first check of the inputs
    status = "boot..."
    
    data_list.clear
    db_val.clear
    
    connection = mysql.connector.connect(host = "localhost", user = groupe, password = pswd, database = database_name)
    task = connection.cursor()
    
    pinSetup()
    
def pinSetup():
    status = "pin settup"
    
    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(cyl_pwm1, GPIO.OUT)
    GPIO.setup(cyl_pwm2, GPIO.OUT) 
    GPIO.setup(cyl_en,GPIO.OUT)
    GPIO.setup(pump,GPIO.OUT)

    GPIO.output(cyl_pwm1,GPIO.LOW)
    GPIO.output(cyl_pwm2,GPIO.LOW)
    GPIO.output(cyl_en,GPIO.LOW)
    GPIO.output(pump,GPIO.LOW)

def reading_data():
    status = "reading data"
    
    request = "SELECT * FROM sensor_data WHERE id = (SELECT MAX(id) FROM sensor_data)"
    task.execute(request,db_val)
    val = task.fetchall()
    
    db_val = list(i for i in val)

def writing_data():
    status = "writing data"  
    
    val = tuple(i for i in data_list)
    request = "INSERT INTO sensor_data (humid_air,humid_ground,temp_in,temp_out,angle,i_pump,v_pump,p_pump,i_cyl,v_cyl,p_cyl,i_bat,v_bat,p_bat,i_solar,v_solar,p_solar,rain,lum,moment)"
    task.execute(request,val)
     
def mode_test():
    #update the variables if switch button change (switch auto/manu, button up, button down, switch pump ON/OFF)
    status = "mode checking"
    
    reading_data()
    
    if db_val[0] == 0:
        mode = 0
        status = "mode Automatic activated"
    else:
        mode = 1
        status = "mode Manual activated"

def measure():
    #Measure of the different input and storing in the data_array
    #[T°air inside - T°air outside - humidity ground - humidity air - T°ground - battery voltage - battery current - battery power - pannel voltage - pannel current - pannel power -
    # pump voltage - pump current - pump power - cylinder voltage - cylinder current - cylinder power - window tiltnessX - window tiltnessY - window tiltnessZ]
    status = "measuring..."
    
    data_list.clear
    
    actual_time = str(datetime.now())
    
    #measure humidity air
    data_list[0] = read_hum(Tins)
    error_check(data_list[0], 0, 100, "01")
    
    #measure humidity ground
    data_list[1] = read_hum(0)
    error_check(data_list[1], 0, 100, "02")
    
    #measure T° air inside
    data_list[2] = read_temp(Tins)
    error_check(data_list[2], -20, 100, "03")
    
    #measure T° air outside
    data_list[3] = read_temp(Tout)
    error_check(data_list[3], -20, 100, "04")
    
    #measure window
    data_list[4] = read_tilt(Tout) 
    error_check(data_list[4], -100, 10, "05")
    
    #measure pump
    data_list[5] = read_volt(pump)
    data_list[6] = read_current(pump)
    data_list[7] = read_power(pump)
    error_check(data_list[7], -10, 10000, "06") 
    
    #measure cylinder
    data_list[8] = read_volt(cyl)
    data_list[9] = read_current(cyl)
    data_list[10] = read_power(cyl)
    error_check(data_list[10], -10, 10000, "07")
    
    #measure battery
    data_list[11] = read_volt(bat)
    data_list[12] = read_current(bat)
    data_list[13] =  read_power(bat)
    error_check(data_list[13], -10, 10000, "08")
    
    #measure solar pannel
    data_list[14] = read_volt(solar)
    data_list[15] = read_current(solar)
    data_list[16] = read_power(solar)
    error_check(data_list[16], -10, 10000, "09")
     
    #measure rain
    data_list[17] = read_rain(rain)
    error_check(data_list[17], 0, 1, "10")
    
    #measure luminosity
    data_list[18] = read_lum(lum)
    
    #measure time
    data_list[19] = actual_time
    
    #send data
    writing_data()

def read_lum(sensor):
    status = "Luminosity reading..."
    
    val = sensor.val
    if val < 1000:
        lumino = 0
    else:
        lumino = math.asin(1000/math.sqrt(33000*33000+1000*1000))*(val-1000)
    
    return lumino

def read_rain(sensor):
    status = "Rain reading..."
    
    if(sensor.val > rain_min):
        israin = 1
    else:
        israin = 0
        
    return israin
    
def read_tilt(sensor):
    #Read tiltness of the window and convert it into °
    status = "Tiltness reading..."
    
    tilt = list(i for i in sensor.acceleration)
    ang = 90*tilt[0]
    
    return ang

def read_volt(sensor):
    #Read voltage of the battery (0), wind turbine (1), solar pannel (2), pump (3), cylinder (4)
    status = "Voltage reading..."
    
    volt = sensor.voltage
    
    return volt

def read_current(sensor):
    #Read current of the battery (0), wind turbine (1), solar pannel (2), pump (3), cylinder (4)
    status = "Current reading..."

    current = sensor.current
    
    return current
    
def read_power(sensor):
    #Read power of the battery (0), wind turbine (1), solar pannel (2), pump (3), cylinder (4)
    status = "Power reading..."
    
    power = sensor.power
    
    return power
    
def read_hum(sensor):
    # Read humidity of ground (0) or air (1) and calculate %
    status = "Humidity reading..."
    
    if(sensor !=0):
        humidity = sensor.relative_humidity
        
    else:
        val = sensor.val
        if val < 20000:
            humidity = 0
        else:
            humidity = math.asin(20000/math.sqrt(97000*97000+20000*20000))*(val-20000) 
    
    return humidity

def read_temp(sensor):
    # Read temperature registers and calculate Celsius
    status = "Temperature reading..."
    
    temp = sensor.temperature
        
    return temp

def output():
    if mode == 0:   #mode Automatic 
        temp_in = read_temp(Tins)
        temp_out = read_temp(Tout)
        tilt = read_tilt(Tout)
        hum_ground = read_hum(hum_ground)
        raining = read_rain(rain)
        
        if temp_in < temp_threshold_max & temp_in < temp_out & tilt < tilt_max:
            status = "Opening the Window"
            
            GPIO.output(cyl_en,GPIO.HIGH) 
            GPIO.output(cyl_pwm1,GPIO.LOW)
            GPIO.output(cyl_pwm2,GPIO.HIGH)
            
            error_check(read_power(cyl), cyl_min, cyl_max, "16")
            error_check(read_tilt(Tout), tilt_min, tilt_max, "16")
            error_check(read_rain(rain), 0,0, 16)
        
        elif (temp_in < temp_threshold_min & temp_in < temp_out & tilt > tilt_min) | (raining != 0):
            status = "Closing the Window"
            
            GPIO.output(cyl_en,GPIO.HIGH)
            GPIO.output(cyl_pwm1,GPIO.HIGH) 
            GPIO.output(cyl_pwm2,GPIO.LOW)
            
            error_check(read_power(cyl), cyl_min, cyl_max, "16")
            error_check(read_tilt(Tout), tilt_min, tilt_max, "16")
            
        else:
            status = "Stop motion"
            
            GPIO.output(cyl_en,GPIO.LOW)
            GPIO.output(cyl_pwm1,GPIO.LOW) 
            GPIO.output(cyl_pwm2,GPIO.LOW) 
            
            error_check(read_power(cyl),-1, cyl_min, "16")
            error_check(read_tilt(Tout), tilt_min, tilt_max, "16")
            
        time.sleep(0.1)
        
        if hum_ground < hum_ground_min: #pump On if not enough water 
            status = "Pump activated"
        
            GPIO.output(pump,GPIO.HIGH)
            
            error_check(read_power(pump), pump_min, pump_max, "17")
            
        elif hum_ground > hum_ground_max:
            status = "Pump desactivated"
            
            GPIO.output(pump,GPIO.LOW)
            
            error_check(read_power(pump), -1, pump_min, "17")
            
        else:
            status = "Pump desactivated"
            
            GPIO.output(pump.GPIO.LOW)
            
            error_check(read_power(pump), -1, pump_min, "17")
            
        time.sleep(0.1)
        
    elif mode == 1: #mode manual
        if db_val[3] == 1 & tilt > tilt_max:
            status = "Opening the Window"
            
            GPIO.output(cyl_en,GPIO.HIGH)
            GPIO.output(cyl_pwm1,GPIO.LOW)
            GPIO.output(cyl_pwm2,GPIO.HIGH)
            
            error_check(read_power(cyl), cyl_min, cyl_max, "16")
            error_check(read_tilt(Tout), tilt_min, tilt_max, "16")
            
        elif db_val[3] == 2 & tilt > tilt_min:
            status = "Closing the Window"
            
            GPIO.output(cyl_en,GPIO.HIGH)
            GPIO.output(cyl_pwm1,GPIO.HIGH)
            GPIO.output(cyl_pwm2,GPIO.LOW)
            
            error_check(read_power(cyl), cyl_min, cyl_max, "16")
            error_check(read_tilt(Tout), tilt_min, tilt_max, "16")
            
        else:
            status = "Stop motion"
            
            GPIO.output(cyl_en,GPIO.LOW)
            GPIO.output(cyl_pwm1,GPIO.LOW)
            GPIO.output(cyl_pwm2,GPIO.LOW)
            
            error_check(read_power(cyl), -1, cyl_min, "16")
            error_check(read_tilt(Tout), tilt_min, tilt_max, "16")
            
        time.sleep(0.1)  
        
        if db_val[2] == 1:
            status = "Pump activated"
          
            GPIO.output(pump.GPIO.HIGH)
            
            error_check(read_power(pump), pump_min, pump_max, "17")
            
        else:
            status = "Pump desactivated"
            
            GPIO.output(pump.GPIO.LOW)
            
            error_check(read_power(pump), -1, pump_min, "17")
            
        time.sleep(0.1)

def error_check(sensor, sensor_threshold, sensor_max, section):
    status = "error checking..."
    
    if sensor < sensor_threshold:
        index = str(3)
    elif sensor > sensor_max:
        index = str(2)
    elif sensor < 0:
        index = str(1)
    else:
        index = str(0)
    error.append(section+index)
    
    return error

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        connection.commit()
        
        print("Error due to ", e)
        
        print("\nError list:\n")
        for i in range (len(error)):
            print (error[i]+"\n" + "during: " + str(status))
            
    finally:
        print('process completed') 

      
                
             
            




        
    


