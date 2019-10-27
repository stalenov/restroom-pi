
# Sortir controller

## OLED connection

Used type: i2c ssd1306

### Enable i2c in Raspberry Pi Debian

Enable:
```
sudo raspi-config > 5 Interfacing Options > P5 I2C
```

Add to /boot/config.txt
```
dtparam=i2c_arm=on,i2c_baudrate=400000
```

Check after reboot:
```
dmesg | grep i2c
```


See also:  https://luma-oled.readthedocs.io/en/latest/hardware.html#identifying-your-serial-interface




Connection

OLED Pin	Name	Remarks	RPi Pin	RPi Function
1	GND	Ground	P01-6	GND
2	VCC	+3.3V Power	P01-1	3V3
3	SCL	Clock	P01-5	GPIO 3 (SCL)
4	SDA	Data	P01-3	GPIO 2 (SDA)

Swith
1 Bath  GPIO17
2 RestRoom GPIO27

Output
1 BathFan GPIO26
2 RestRoomFan GPIO19
2 RestRoomSmell GPIO13 


Pin mappings schema: https://docs.microsoft.com/en-us/windows/iot-core/learn-about-hardware/pinmappings/pinmappingsrpi



## Install and configure required software

sudo usermod -a -G spi,gpio pi
sudo usermod -a -G spi,gpio ks

sudo apt install python3-dev python3-pip libfreetype6-dev libjpeg-dev build-essential libopenjp2-7 libtiff5 python-rpi.gpio
# sudo -H pip3 install --upgrade luma.oled

pip3 install -r requrements.txt