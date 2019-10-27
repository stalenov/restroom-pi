#!/bin/bash

# ssh pi mkdir -p /home/pi/restroom-pi/fonts/

# scp -r /home/ks/code/restroom-pi/fonts pi:/home/pi/restroom-pi/
scp -r /home/ks/code/restroom-pi/main.py pi:/home/pi/restroom-pi/
# scp -r /home/ks/code/restroom-pi/requirements.txt pi:/home/pi/restroom-pi/

ssh pi python3 /home/pi/restroom-pi/main.py
