import os
import time
import sys
import datetime

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from PIL import ImageFont
import RPi.GPIO as GPIO


# setup font for lcd display
font_file = "Volter__28Goldfish_29.ttf"
# font_file = "code2000.ttf"
fonts_folder = "fonts"
font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                fonts_folder, font_file))
font = ImageFont.truetype(font_path, 16)

# setup i2c interface for LCD
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, rotate=0)

# setup GPIO
I_BATH_SW = 17
I_RESTROOM_SW = 27
O_BATH_FAN = 26
O_BATH_HEATER = 6
O_RESTROOM_FAN = 19
O_RESTROOM_AIR = 13

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(O_BATH_FAN, GPIO.OUT)
GPIO.setup(O_RESTROOM_FAN, GPIO.OUT)
GPIO.setup(O_RESTROOM_AIR, GPIO.OUT)
GPIO.setup(O_BATH_HEATER, GPIO.OUT)

GPIO.setup(I_BATH_SW, GPIO.IN)
GPIO.setup(I_RESTROOM_SW, GPIO.IN)


count_bath_fan = 0
count_bath_sw = 0
count_restroom_fan = 0
count_restroom_sw = 0
count_bath_heater = 0

DELAY_RESTROOM_SW_1 = 5
DELAY_RESTROOM_FAN_1 = 30
DELAY_RESTROOM_SW_2 = 10 #60
DELAY_RESTROOM_FAN_2 = 30 #300
DELAY_BATH_SW = 0
DELAY_BATH_FAN = 30 # 300
DELAY_BATH_HEATER = 45 #900

while True:
    # RESTROOM
    if GPIO.input(I_RESTROOM_SW):
        print("RestRoom")
        count_restroom_sw += 1
        if count_restroom_sw > DELAY_RESTROOM_SW_1:
            count_restroom_fan = DELAY_RESTROOM_FAN_1
        if count_restroom_sw > DELAY_RESTROOM_SW_2:
            count_restroom_fan = DELAY_RESTROOM_FAN_2
    else:
        count_restroom_sw = 0

    if count_restroom_fan > 0:
        GPIO.output(O_RESTROOM_FAN, GPIO.HIGH)
        count_restroom_fan -= 1
    else:
        GPIO.output(O_RESTROOM_FAN, GPIO.LOW)

    # BATH
    if GPIO.input(I_BATH_SW):
        print("Bath")
        count_bath_sw += 1
        if count_bath_sw > DELAY_BATH_SW:
            count_bath_fan = DELAY_BATH_FAN
            count_bath_heater = DELAY_BATH_HEATER
    else:
        if count_bath_sw > 0:
            GPIO.output(O_RESTROOM_AIR, GPIO.HIGH)
        count_bath_sw = 0
        GPIO.output(O_RESTROOM_AIR, GPIO.LOW)

    if count_bath_fan > 0:
        GPIO.output(O_BATH_FAN, GPIO.HIGH)
        count_bath_fan -= 1
    else:
        GPIO.output(O_BATH_FAN, GPIO.LOW)

    if count_bath_heater > 0:
        GPIO.output(O_BATH_HEATER, GPIO.HIGH)
        count_bath_heater -= 1
    # disabled only by main scheduler
    #else:
    #    GPIO.output(O_BATH_HEATER, GPIO.LOW)

    # OUTPUT TO LCD
    with canvas(device) as draw:
        cur_time = time.localtime(time.time())
        cur_time_msg = "{}.{}.{}".format(cur_time[3], cur_time[4], cur_time[5])

        draw.rectangle(device.bounding_box, outline="black", fill="black")
        # show current time
        draw.text((0, 0), cur_time_msg, font=font, fill="white")

        # count_bath_fan
        # count_bath_sw
        # count_restroom_fan
        # count_restroom_sw
        # count_bath_heater

        bath_msg = "B: {}:{}:{}".format(count_bath_sw, count_bath_fan, count_bath_heater)
        draw.text((0, 20), bath_msg, font=font, fill="white")

        restroom_msg = "RR: {}:{}".format(count_restroom_sw, count_restroom_fan)
        draw.text((0, 40), restroom_msg, font=font, fill="white")

    time.sleep(1)
