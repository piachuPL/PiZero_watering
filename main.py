import  time
import datetime
import logging
import paho.mqtt.client as mqtt
from secrets import *                                   #import secret passwords :D
import requests
import bs4 as bs 

HH = 21
MM = 00                               


### Loging 
logging.basicConfig(filename='myapp.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.info('Started')


### GPiO
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
valves= [['zawor1',37,600],['zawor2',35,600],['zawor3',33,600]]             #[1,37,20] = 1=valve 37 = GPIO 20 = min ON
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
        print('otwieram : '+ str(x[0]))                 #printing opening valve1...2...3...
        print('otwarcie gpio :'+ str(x[1]))             # printing 'opening GPIO Port
        logging.info('otwieram : '+ str(x[0]))          #log
        GPIO.setup(x[1], GPIO.OUT)                      #set GPIO
        GPIO.output(x[1], GPIO.LOW)                    #Set 1
        msd_mqtt(str(x[0]), 'ON')                       # send msg MQTT
        time.sleep(x[2])                                #
        print('zamkn gpio :'+ str(x[1]))
        GPIO.output(x[1], GPIO.HIGH)
        print('zamkniety: '+ str(x[0]))
        logging.info('zamkniety : '+ str(x[0]))
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

### sunset geting from site meteocast.net hour of sunset and returning in format HH MM.
def sunset(sleep_time):
    try:
        resp = requests.get(meteocast_url)                    #url in secrets 
        soup = bs.BeautifulSoup(resp.text, 'html.parser')
        table = soup.find('a', {'class':'wdn'})
        hour = table.findAll('b')[2].text
        HH = hour[0]+hour[1]
        MM = hour[3]+hour[4]
        time.sleep(sleep_time)                                    #sleep to make req only once
        return int(HH), int(MM)
        logging.info('Zachod słonca o: {}:{}'.format(HH, MM))
    except:
        print('sunset() error')
        logging.info('sundet() error')

###GPIO reload sequence on start  
for i in valves:
        GPIO.setup(i[1], GPIO.OUT)
        GPIO.output(i[1], GPIO.LOW)
        time.sleep(1)
        GPIO.output(i[1], GPIO.HIGH)
        time.sleep(1)

HH, MM = sunset(1)

while True:
#    now = datetime.datetime.now()
#    zm = datetime.time(now.hour, now.minute, now.second)

#    print(zm)
    time.sleep(1)
    if time_now() == datetime.time(12, 00):              #sunset update time
            HH, MM = sunset(60)
            print(HH, MM)      
#    print('od poczatku')
    while GPIO.input(3) == 0:
#    while gpio_rain == 1:                              # only for testing
      
        print('pada')
        if delay_time == 6:
                msd_mqtt('rain_sensor', 'ON')
        time.sleep(2)
        delay_time += 2
        print(delay_time)
#        if delay_time == 12:                           # only for testing
#            gpio_rain = 0                              # only for testing
    else:
         
        if delay_time>0:
                if delay_time == 2:
                        msd_mqtt('rain_sensor', 'OFF')
                delay_time -= 2
                time.sleep(2)
                print('ziemia wilgotna '+ str(delay_time))
        else:

                if time_now() == datetime.time(HH,MM): #Setting when watering starts
                        start_time = time_now()
                        print ('Zaczynam Podlewanie: ' + str(start_time) )
                        watering()



