from threading import Thread #Kør flere loops samtidigt
import time
import datetime
import os
import serial
import schedule #Planlæg at kalde funktioner ved et interval
from csv import writer

from picamera2 import Picamera2 

#Disse moduler bruges til fluxgate
import board
import adafruit_ads1x15.ads1115 as ADS 
from adafruit_ads1x15.analog_in import AnalogIn
import busio

import RPi.GPIO as GPIO #RPi PIN - læser LED og Knap


class Bird():
    def mag_initialize(self):
        print("Initializing fluxgate")
        # Create the I2C bus
        self.i2c = busio.I2C(board.SCL, board.SDA)
        # Create the ADC object using the I2C bus
        #ads = ADS.ADS1015(self.i2c) 
        self.ads = ADS.ADS1115(self.i2c)

        # Create 3 inputs on channel 0,1,2
        self.chan = AnalogIn(self.ads, ADS.P0)
        self.chan1 = AnalogIn(self.ads,ADS.P1)
        self.chan2 = AnalogIn(self.ads,ADS.P2)

    def gps_initialize(self):
        print("Initalizing GPS/IMU")
        self.ser = serial.Serial()
        #Der angives en bestemt baudrate, som kan findes under oplysninger af GPS'en (skal forstås som hastigheden af komunikationen)
        self.ser.baudrate = 460800
        self.ser.port = '/dev/ttyUSB0'
        self.ser.open()
        print("Serial port is open:", self.ser.isOpen())
    
    def camera_initialize(self):
        print("Initializing Camera")
        # Initialiser PiCamera
        self.picam2 = Picamera2()

        # Her kan du ændre resoulution 
        self.config = self.picam2.create_still_configuration({"size": (4056, 3040)})

        # Starter kamerater op
        self.picam2.configure(self.config)
        self.picam2.start()
    
    def add_event(self):
        GPIO.add_event_detect(self.knap_GPIO, GPIO.FALLING, callback=self.button_pressed_callback, bouncetime=200)

    def __init__(self):
        # Instance Variable
        self.flag = False
        self.mag_initialize()
        self.gps_initialize()
        self.camera_initialize()
        #sheduler at køre "write.time" hvert 0.1s (til tidssync af GMU)
        schedule.every(0.1).seconds.do(self.write_time)

    def voltage_conversion_x(self):
        return(self.chan.voltage*3.9851-8.2431)

    def voltage_conversion_y(self):
        return(self.chan1.voltage*3.9801-8.2388)    
    
    def voltage_conversion_z(self):
        return(self.chan2.voltage*3.9841-8.247) 
        
    def convert_to_tesla(self,voltage):
        return (voltage*90/8)

    def magnetometer(self):
        while self.flag:
            self.x_voltage = self.voltage_conversion_x()
            self.y_voltage = self.voltage_conversion_y()
            self.z_voltage = self.voltage_conversion_z()
            self.tesla0 = self.convert_to_tesla(self.chan.voltage)
            self.tesla1 = self.convert_to_tesla(self.chan1.voltage)
            self.tesla2 = self.convert_to_tesla(self.chan2.voltage) 
            self.magnetData = [datetime.datetime.now(),self.chan.voltage,self.chan1.voltage,self.chan2.voltage,self.x_voltage,self.y_voltage,self.z_voltage,self.tesla0,self.tesla1,self.tesla2]
            print("tid:",datetime.datetime.now(),"X_raw: ",self.chan.voltage,"Y_raw",self.chan1.voltage,"Z_raw",self.chan2.voltage,"X_volt: ",self.x_voltage,"Y_volt",self.y_voltage,"Z_volt",self.z_voltage,"x_tesla",round(self.tesla0,3),"y_tesla",round(self.tesla1,3),"z_tesla",round(self.tesla2,3))
            with open(self.path+"/magdata.csv","a", newline='') as self.magnet_fil:  
                # Pass the CSV  file object to the writer() function
                writer_object = writer(self.magnet_fil)
                # Result - a writer object
                # Pass the data in the list as an argument into the writerow() function
                writer_object.writerow(self.magnetData)  
                # Close the file object
                self.magnet_fil.close()

    def write_time(self):
        self.tidsfil.write(str(datetime.datetime.now())+"\n")
        self.tidsfil.flush()

    def gps_tracker(self):
        while self.flag:
            print("Measuring GPS at",datetime.datetime.now())
            self.mchar = self.ser.read()
            self.gpsfile.write(self.mchar)
            self.gpsfile.flush()
            schedule.run_pending()

    def tagbillede(self):
        while self.flag:
            # Generer filnavn baseret på tidspunktet for billedet
            self.billedename = 'image_{}.jpg'.format(time.strftime('%Y%m%d-%H%M%S'))
            
            # Tag et billede og gem det med det genererede filnavn. (Hvis den ikke virker, så prøv den kommando under, ved at fjerne "#", og så sætte det foran den den nuværende hvis den ik virker)
            self.picam2.capture_file(self.path+"/billeder/" + self.billedename)
            print("Picture taken at ",datetime.datetime.now())
            self.billedetid.write(str(datetime.datetime.now())+"\n")
            self.billedetid.flush()

    # Create and start the threads
    def begin_threads(self):
        if self.flag:
            thread1 = Thread(target=self.tagbillede,args=())
            thread2 = Thread(target=self.gps_tracker,args=())
            thread3 = Thread(target=self.magnetometer,args=())
            thread1.start()
            thread2.start()
            thread3.start()

    #laver ny mappe og filer til al data
    def update_path(self):
        if self.flag:
            self.path = "/media/magneten/KINGSTON/"+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            os.mkdir(self.path)
            os.mkdir(self.path+"/billeder/")
            
            #lav header på CSV filen
            self.magnet_header = ["tid","x_rå","y_rå","z_rå","x_volt","y_volt","z_volt","x_tesla","y_tesla","z_tesla"]
            with open(self.path+"/magdata.csv","a", newline='') as self.magnet_fil:  
                writer_object = writer(self.magnet_fil)
                writer_object.writerow(self.magnet_header)  
                self.magnet_fil.close()

            #Der laves en ny fil med filtypen .anpp (log converteren i Spatial Manager kan kun modtage den her filtype). Det skal være i bytes, dermed wb (write byte)
            self.gpsfile = open(self.path+"/IMUdata.anpp","wb")
            #Der laves også en tidsfil, som logger ved hvilke interne rasp pi tider data gemmes.
            self.tidsfil = open(self.path+"/IMUtid.txt","w")
            self.billedetid = open(self.path+"/billedetider_{}.txt".format(time.strftime('%Y%m%d-%H%M%S')),"w")
            print("New Path was created!")

state = False
#Kaldes ved tryk på knap
def button_pressed_callback(channel):
    global state
    print("Button was pressed at ",datetime.datetime.now())
    print(state)
    if state == 2:
        state = False
    elif state == 3:
        state = True
        
knap_GPIO = 23
LED_GPIO = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(knap_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_GPIO,GPIO.OUT)

def main():
    global state
    T = Bird()
    #T.begin_threads()
    GPIO.add_event_detect(knap_GPIO, GPIO.FALLING, callback=button_pressed_callback, bouncetime=200)
    
    while True:
        if state == True:
            GPIO.output(LED_GPIO,GPIO.HIGH) #LED'en tændes
            T.flag = True
            T.update_path()
            T.begin_threads()
            state = 2
        elif state == False:
            GPIO.output(LED_GPIO,GPIO.LOW) # LED'en slukkes
            T.flag = False
            state  = 3
        else: 
            pass
    #T.add_event()

    #Ends script after user input
    input("Press enter to exit.")
    del T
    GPIO.cleanup()

if __name__ == "__main__":
    main()
