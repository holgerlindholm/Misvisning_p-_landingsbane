import time
import datetime
import board
import adafruit_ads1x15.ads1115 as ADS 
import math
from adafruit_ads1x15.analog_in import AnalogIn
import busio

import serial
global ser
import os 

import schedule
import pandas as pd

from pynput.keyboard import Key, Listener

path = "/home/magneten/Desktop/{}".format(time.strftime('%Y%m%d-%H%M%S'))
os.mkdir(path)

def convert_to_tesla(voltage):
    factor = 11.6*2
    return(voltage * factor)
   
def magnet(angle):
    tesla0 = convert_to_tesla(chan.voltage)
    tesla1 = convert_to_tesla(chan1.voltage)
    tesla2 = convert_to_tesla(chan2.voltage) 
    styrke = math.sqrt(tesla0**2+tesla1**2+tesla2**2)
    print("tid:",datetime.datetime.now(),"Digital Value",chan.value,"X pin0: ",chan.voltage,"Y pin1:",chan1.voltage,"Z pin2:",chan2.voltage,"Styrke:",styrke)
    data = (1,angle,tesla0,tesla1,tesla2,styrke,chan.voltage,chan1.voltage,chan2.voltage,1)
    file.write(str(data)+"\n")
    file.flush()

     
start = time.time()
# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)
# Create the ADC object using the I2C bus
#ads = ADS.ADS1015(i2c)
ads = ADS.ADS1115(i2c)

# Create 3 inputs on channel 0,1,2
chan = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads,ADS.P1)
chan2 = AnalogIn(ads,ADS.P2)


start = round(time.time(),4)

magnetdata = [("vinkel","X","Y","Z","styrke","råx","råy","råz")] 

angle = 0
count = [] 
file = open(path+"/KALIBRERINGdata_{}.txt".format(time.strftime('%Y%m%d-%H%M%S')),"w")

def show(key):
	if key==Key.space:
         magnet(angle+sum(count))
         count.append(1)
        
	
with Listener(on_press = show) as listener:
	listener.join()






   
