import time
import pycom
from machine import Pin
#from LoraMAC import sendtoLoRa
from dht22 import DHT22
from bmp180 import BMP180
from machine import I2C

def go_DHT():
    dht_pin=Pin('G10', Pin.OPEN_DRAIN)	# connect DHT22 sensor data line to pin P9/G16 on the expansion board
    dht_pin(1)							# drive pin high to initiate data conversion on DHT sensor

    while (True):
        temp, hum = DHT22(dht_pin)
        temp_str = '{}.{}'.format(temp//10,temp%10)
        hum_str = '{}.{}'.format(hum//10,hum%10)
        # Print or upload it
        print('temp = {}C; hum = {}%'.format(temp_str, hum_str))
        # if hum!=0xffff:
        #     sendtoLoRa(dev_ID,  temp,  hum)
        sda_pin = Pin('G16', Pin.OPEN_DRAIN)
        scl_pin = Pin('G17', Pin.OPEN_DRAIN)
        bus = I2C(0)
        #sda = sda_pin, scl = scl_pin)
        bus.init(I2C.MASTER, baudrate=100000)           # on pyboard
        # bus =  I2C(scl=Pin(4), sda=Pin(5), freq=100000)   # on esp8266
        bmp180 = BMP180(bus)
        bmp180.oversample_sett = 0
        #bmp180.baseline = 101325

        temp = bmp180.temperature
        p = bmp180.pressure
        altitude = bmp180.altitude
        sl_pressure = bmp180.sea_level_pressure
        print(temp, p, sl_pressure, altitude)
        time.sleep(2)

pycom.heartbeat(False)
pycom.rgbled(0x000000)    # turn LED blue


# f=open('device_name.py')   #get device name from file
# dev_ID = f.read()
# print(dev_ID)

go_DHT()
