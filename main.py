import  time
import datetime
import logging
import paho.mqtt.client as mqtt
from astral import Astral
from secrets import *                                   #import secret passwords :D


HH = 19
MM = 10                               


### Loging 
logging.basicConfig(filename='p_LOG.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
logging.info('Started')


### GPiO
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
valves= [['zawor1',37,150],['zawor2',35,150],['zawor3',33,150]]             #[1,37,20] = 1=valve 37 = GPIO 20 = min ON
GPIO.setup(3, GPIO.IN)
delay_time=0
gpio_rain = 0                                       # ## when GPIO working


### MQTT 
Connected = False
broker_adress = mqtt_adress
user = mqtt_user
password = mqtt_password
client = mqtt.Client("Python")
client.username_pw_set(user,password=password)


######## Functions

### MSG publish in MQTT
def msd_mqtt(valve, msg):
    client.connect(broker_adress)
    client.publish("stat/spalona/" + valve , msg)


### GPIO sequence opening valve one by one 
def watering():
    for x in valves:
        print('otwieram : '+ str(x[0]))                         #printing opening valve1...2...3...
        print('otwarcie gpio :'+ str(x[1]))                     # printing 'opening GPIO Port
        logging.info('otwieram : {}'.format(str(x[0])))         #log
        GPIO.setup(x[1], GPIO.OUT)                              #set GPIO
        GPIO.output(x[1], GPIO.LOW)                             #Set 1
        msd_mqtt(str(x[0]), 'ON')                               # send msg MQTT
        time.sleep(x[2])                                        #
        print('zamkn gpio :'+ str(x[1]))
        GPIO.output(x[1], GPIO.HIGH)
        print('zamkniety: '+ str(x[0]))
        logging.info('zamkniety : {}'.format(str(x[0])))
        msd_mqtt(str(x[0]), 'OFF')
        time.sleep(3)


### Returning a time HH:MM
def time_now():
    now = datetime.datetime.now()
    time_now_HMS = datetime.time(now.hour, now.minute)
#    print(time_now_HMS)
#    time.sleep(1)
    return time_now_HMS
start_time = time_now()
print('Start APP : ' + str(start_time))

### sunset() geting from astral hour of sunset and returning in format HH MM.
def sunset(sleep_time):
    city_name = 'Warsaw'
    a = Astral()
    a.solar_depression = 'civil'
    city = a[city_name]
    today = datetime.datetime.now()

    sun = city.sun(date=today, local=True)
    time.sleep(sleep_time)
    
    str_sun = str(sun['dusk'])
    HH = int(str_sun[11:13])
    MM = int(str_sun[14:16])
    logging.info('Dzis {}.{}.{} zmierzch jest o {}:{}.'.format(today.day, today.month, today.year,HH, MM))
    return HH, MM

HH, MM = sunset(1)


###GPIO reload sequence on start  
for i in valves:
        GPIO.setup(i[1], GPIO.OUT)
        GPIO.output(i[1], GPIO.LOW)
        time.sleep(1)
        GPIO.output(i[1], GPIO.HIGH)
        time.sleep(1)


while True:
#    now = datetime.datetime.now()
#    zm = datetime.time(now.hour, now.minute, now.second)

#    print(zm)
    time.sleep(1)
    if time_now() == datetime.time(12, 30):              #sunset update time
            HH, MM = sunset(60)


    while GPIO.input(3) == 0:
#    while gpio_rain == 1:                              # only for testing
      
        print('pada')
        if delay_time == 6:
                logging.info('Zaczelo padac')
                msd_mqtt('rain_sensor', 'ON')
        time.sleep(2)
        delay_time += 2
        print(delay_time)
#        if delay_time == 12:                           # only for testing
#            gpio_rain = 0                              # only for testing
    else:
         
        if delay_time>0:
                if delay_time == 2:
                        logging.info('Przestalo padac')
                        msd_mqtt('rain_sensor', 'OFF')
                delay_time -= 2
                time.sleep(2)
                print('ziemia wilgotna {}'.format(str(delay_time)))
                
        else:

                if time_now() == datetime.time(HH,MM): #Setting when watering starts
                        start_time = time_now()
                        print ('Zaczynam Podlewanie: {}'.format(str(start_time)))
                        logging.info('Podlewanie')
                        watering()



