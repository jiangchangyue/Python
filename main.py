import sensor, image
import time
from pyb import Pin
pin1 = Pin('P1', Pin.OUT_PP, Pin.PULL_NONE)
pin0 = Pin('P0', Pin.OUT_PP, Pin.PULL_NONE)
white_threshold = (80, 90, 0, 0, 0, 0)
blue_threshold = ((40, 50, 0, 20, -40, -20))
green_threshold = (54, 67, -50,-36, 4, 21)
red_threshold = (65,75,30,45,5,15)
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(100)
sensor.set_auto_whitebal(False)
clock = time.clock()
a=0
b=0
c=0
d=0
while(True):
	clock.tick()
	img = sensor.snapshot()
	white_blob = img.find_blobs([white_threshold])
	blue_blob = img.find_blobs([blue_threshold])
	green_blob = img.find_blobs([green_threshold])
	red_blob = img.find_blobs([red_threshold])
	if white_blob:
		a=a+1
		print("a type is %s"%a)
		if(a==4):
			pin0.value(0)
			pin1.value(0)
			print('white')
			a=0
	elif  blue_blob:
	   b=b+1
	   print("b type is %s"%b)
	   if(b==4):
		   pin0.value(1)
		   pin1.value(0)
		   print('blue')
		   b=0
	elif green_blob:
		c=c+1
		print("c type is %s"%c)
		if(c==4):
		   pin0.value(1)
		   pin1.value(1)
		   print('green')
		   c=0
	elif red_blob:
		 d=d+1
		 print("d type is %s"%d)
		 if(d==4):
			pin0.value(0)
			pin1.value(1)
			print('red')
			d=0
	print(clock.fps())
