#Dette script kører IMU og stopper det når man trykker "enter"
#Der importeres pakker:
import time
import serial
import math
import datetime
import os
import schedule
from pynput import keyboard

#Der laves en global variabel som benyttes til serialporten:
global ser

#Der laves en ny mappe med en bestemt tidsbaseret path, hvor dataet gemmes i:
path = "/media/magneten/KINGSTON/GPS{}".format(time.strftime('%Y%m%d-%H%M%S'))
os.mkdir(path)

#Serial initialiseres
ser = serial.Serial()
#Der angives en bestemt baudrate, som kan findes under oplysninger af GPS'en (skal forstås som hastigheden af komunikationen)
ser.baudrate = 460800
ser.port = '/dev/ttyUSB0'
ser.open()
print("Serial port is open:", ser.isOpen())
#Der laves en ny fil med filtypen .anpp (log converteren i Spatial Manager kan kun modtage den her filtype). Det skal være i bytes, dermed wb (write byte)
file = open(path+"/IMUdata.anpp","wb")
#Der laves også en tidsfil, som logger ved hvilke interne rasp pi tider data gemmes.
tidsfil = open(path+"/IMUtid.txt","w")

#En funktion til at stoppe scriptet nemt (ved at trykke på "enter")
def on_press(key):
    if key==keyboard.Key.enter:
        print("stop")
        return False  #Stopper 'listener' nede i while loopet

#Funktion til at logge tiden.
def write_time():
     tidsfil.write(str(datetime.datetime.now())+"\n")
     tidsfil.flush()

#Da IMU'en har et internt delay skal det manuelt configureres for tidsfilen
schedule.every(0.1).seconds.do(write_time)

with keyboard.Listener(on_press=on_press) as listener:
    while True:
        #Der læses data fra IMU'en
        mchar = ser.read()
        file.write(mchar)
        # .flush() er en nyttig kommando, da datafilen hele tiden opdateres i et uendeligt while loop - filen kan ellers ikke lukkes.
        file.flush()
        schedule.run_pending()
        
        
        #Vil stoppe scriptet når 'enter' trykkes eller når 'listener' stoppes (nyttigt til tests)
        if not listener.running:
            break  #Forlader loopet


print("FINISH")
