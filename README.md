# Misvisning på landingsbane

### Scripts
**main.py** kører on boot og styrer følgende scripts:
- **magnetometer** logger flux-gate dataen som .csv
- **tagbillede** tager billeder med pycamera
- **gps** logger IMU data og gemmer det som .anpp samt tid i .csv

### Installation
#### pip install
Alle dependencies er installeret med **pip install** fra rasp-pi. (Husk at rasp-pi skal have internetforbindelse!)
#### Autoboot
Følg <a href="https://www.makeuseof.com/how-to-run-a-raspberry-pi-program-script-at-startup/#run-gui-programs-on-startup-with-autostart">denne vejledning</a> til at køre et program, når rasp-pi booter.

1. Lav en fil i mappen /etc/xdg/autostart/ og kald den filnavn.desktop
2. Tilføj følgende til filnavn.desktop: 
  ```sh
[Desktop Entry]
Name=PiCounter
Exec=/usr/bin/python3 /home/pi/magneten/main.py
  ```
I dette tilfælde hedder brugeren "magneten" og filen hedder "main.py"

3. Tryk **CTR + O** for at gemme filen og skriv **sudo reboot** i terminalen for at genstarter Raspberry Pi

####

### Kamera
For at kameraet virker skal raspberry konfigureres:
1. Skriv følgende i terminal
  ```sh
sudo raspi-config
  ```
2. Tryk på interface og slå "legacy camera mode" fra
3.  ```sudo reboot ```
### Elektrisk kredsløb
<p align="center">
  <img src="assets/kredsløb.png" height=500>
</p>
