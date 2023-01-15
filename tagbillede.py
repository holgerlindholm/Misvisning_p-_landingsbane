import time
import datetime
from picamera2 import Picamera2
import os 
import schedule
from pynput import keyboard

# Initialiser PiCamera
picam2 = Picamera2()

# Her kan du ændre resoulution 
config = picam2.create_still_configuration({"size": (4056, 3040)})

# Starter kamerater op
picam2.configure(config)
picam2.start()

path = "/media/magneten/KINGSTON/BILLEDE{}".format(time.strftime('%Y%m%d-%H%M%S'))
os.mkdir(path)
os.mkdir(path+"/billeder/")

def tagbillede():
   # Generer filnavn baseret på tidspunktet for billedet
   filename = 'image_{}.jpg'.format(time.strftime('%Y%m%d-%H%M%S'))

   # Tag et billede og gem det med det genererede filnavn. (Hvis den ikke virker, så prøv den kommando under, ved at fjerne "#", og så sætte det foran den den nuværende hvis den ik virker)
   picam2.capture_file(path+"/billeder/" + filename)
   print("Picture taken at ",datetime.datetime.now())
   billedetid.write(str(datetime.datetime.now())+"\n")
   billedetid.flush()
   
def on_press(key):
    if key==keyboard.Key.enter:
        print("stop")
        return False  # stop the listener
    
schedule.every(0.5).seconds.do(tagbillede)

billedetid = open(path+"/tider_{}.txt".format(time.strftime('%Y%m%d-%H%M%S')),"w")
start = round(time.time(),4)

with keyboard.Listener(on_press=on_press) as listener:
    while True:
        schedule.run_pending()
        
        # this will block until the Enter key is pressed or the listener is stopped
        if not listener.running:
            break  # exit the loop

# Stop PiCamera2
picam2.close()

# Udskriv tidspunktet for afslutningen af scriptet
print('Completed at {}'.format(time.strftime('%Y-%m-%d %H:%M:%S')))
   
