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
from pynput import keyboard
from csv import writer

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
    
path = "/media/magneten/KINGSTON/MAG{}".format(time.strftime('%Y%m%d-%H%M%S'))
os.mkdir(path)
magfile = open(path+"/magdata.csv","w")

#lav header på CSV filen
magnet_header = ["tid","x_rå","y_rå","z_rå","x_volt","y_volt","z_volt","x_tesla","y_tesla","z_tesla"]
with open(path+"/magdata.csv","a", newline='') as magnet_fil:  
    writer_object = writer(magnet_fil)
    writer_object.writerow(magnet_header)  
    magnet_fil.close()
    
def voltage_conversion_x(voltage):
    return(voltage*3.9851-8.2431)
    
def voltage_conversion_y(voltage):
    return(voltage*3.9801-8.2388)    
    
def voltage_conversion_z(voltage):
    return(voltage*3.9841-8.247)
    
        
def convert_to_tesla(voltage):
    return (voltage*90/8)
    
def magnet():
    x_voltage = voltage_conversion_x(chan.voltage)
    y_voltage = voltage_conversion_y(chan1.voltage)
    z_voltage = voltage_conversion_z(chan2.voltage)
    tesla0 = convert_to_tesla(x_voltage)
    tesla1 = convert_to_tesla(y_voltage)
    tesla2 = convert_to_tesla(z_voltage) 
    
    magnetData = [datetime.datetime.now(),chan.voltage,chan1.voltage,chan2.voltage,x_voltage,y_voltage,z_voltage,tesla0,tesla1,tesla2]
    print("tid:",datetime.datetime.now(),"X_raw: ",chan.voltage,"Y_raw",chan1.voltage,"Z_raw",chan2.voltage,"X_volt: ",x_voltage,"Y_volt",y_voltage,"Z_volt",z_voltage,"x_tesla",round(tesla0,3),"y_tesla",round(tesla1,3),"z_tesla",round(tesla2,3))
    with open(path+"/magdata.csv","a", newline='') as magnet_fil:  
        # Pass the CSV  file object to the writer() function
        writer_object = writer(magnet_fil)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(magnetData)  
        # Close the file object
        magnet_fil.close()

def on_press(key):
    if key==keyboard.Key.enter:
        print("stop")
        file = pd.DataFrame(data=magnetdata)
        file.to_csv(path+"/data_{}.csv".format(time.strftime('%Y%m%d-%H%M%S')),mode="a",float_format="%.6f",header=False,index=0)
        return False  # stop the listener
     


with keyboard.Listener(on_press=on_press) as listener: #Stops script on enter
    while True:
        magnet()
        #print("..")
        # this will block until the Enter key is pressed or the listener is stopped
        if not listener.running:
            break  # exit the loop

