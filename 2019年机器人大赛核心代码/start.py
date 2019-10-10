#!/usr/bin/python
import smbus
import math
import types
import ctypes
import time
import subprocess
import RPi.GPIO as gpio
bus = smbus.SMBus(1) 
addr1= 0x51
import sys

import serial

ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)
print ser.isOpen()

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

gpio_number1=22
gpio_number2=36
gpio.setup(gpio_number1,gpio.IN)
gpio.setup(gpio_number2,gpio.IN)

ser.write("{#000P1490T1000!#001P1630T1000!#002P1170T1000!#003P1180T1000!#004P1490T1000!#005P1170T1000!#006P1410T1000!#007P0990T1000!#008P1490T1000!#009P1350T1000!#010P1810T1000!#011P1810T1000!#012P1490T1000!#013P1770T1000!#014P1980T1000!#015P1620T1000!#016P1500T1000!#017P0000T1000!#018P0000T1000!#019P0000T1000!#020P1610T1000!#021P1610T1000!#022P0000T1000!#023P0000T1000!#024P0000T1000!#025P0000T1000!#026P0000T1000!#027P0000T1000!#028P0000T1000!#029P0000T1000!#030P0000T1000!}\n\r")
time.sleep(1.010)

def calc_angle_value(x_angle,y_angle,z_angle):
	t = 0
	global flag
	x = (((x_angle[1] << 8) | x_angle[0]))/32768.0*180.0
	y = (((y_angle[1] << 8) | y_angle[0]))/32768.0*180.0
	z = (((z_angle[1] << 8) | z_angle[0]))/32768.0*180.0
	
	print(x,y,z)

def ReadData(address):
	t = 0
	x_angle = bus.read_i2c_block_data(address,0x3d,2)
	y_angle = bus.read_i2c_block_data(address,0x3e,2)
	z_angle = bus.read_i2c_block_data(address,0x3f,2)
	t= calc_angle_value(x_angle,y_angle,z_angle)
	return t

while(1):
	while(1):
		try:
			t = ReadData(addr1)
			if(t == 2):
				break
		except ValueError:
			continue
		time.sleep(0.2)
	while(1):
		weiyi()

