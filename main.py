import time
#time.sleep(10)
import signal
import sys
import RPi.GPIO as GPIO
import subprocess

#Initialisering af knap + LED
GPIO.setwarnings(False)
knap_GPIO = 23
LED_GPIO = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(knap_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_GPIO,GPIO.OUT)

state = []
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def button_pressed_callback(channel):
    if len(state) == 0: #Når man trykket på knappen første gang er længden af 'state' 0, og dette vil køre:
        state.extend([1]) #'state' forlænges en gang
        GPIO.output(LED_GPIO,GPIO.HIGH) #LED'en tændes
        
    elif len(state) == 2: #Efter scripts er startet vil  længden af 'state' være 2, og dette vil køre når der trykkes på knappen igen:
        state.extend([1]) #'state' forlænges en gang
        GPIO.output(LED_GPIO,GPIO.LOW) # LED'en slukkes

GPIO.add_event_detect(knap_GPIO, GPIO.FALLING, callback=button_pressed_callback, bouncetime=200)

while True: #Main loop
    #'state' vil have en længde på 1, når LED'en er tændt
    if len(state) == 1: 
        #Kører de tre scripts når man har trykket på knappen
        sub = subprocess.Popen(["python3","/home/magneten/Desktop/Scripts/magnetometer.py"])
        sub2 = subprocess.Popen(["python3","/home/magneten/Desktop/Scripts/gps.py"])
        sub3 = subprocess.Popen(["python3","/home/magneten/Desktop/Scripts/tagbillede.py"])
        state.extend([1]) #'state' forlænges en gang igen
        print(state)
        
    elif len(state) == 3: #'state' vil have en længde på 3, når LED'en er slukket
        #Stopper de tre scripts når man trykket på knappen igen
        sub.kill()
        sub2.kill()
        sub3.kill()
        del state[0:3] #Alt i 'state' fjernes, og man kan tænde LED'en igen (og dermed starte scripts igen) ved at trykke igen
        print(state)
