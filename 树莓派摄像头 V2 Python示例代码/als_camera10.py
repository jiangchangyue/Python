#添加不同颜色的字符，例程中底色使用蓝色，字体使用黄色，显示文字“hello world”
from picamera import PiCamera, Color
from time import sleep

camera = PiCamera()
camera.start_preview()
camera.annotate_background = Color('blue')
camera.annotate_foreground = Color('yellow')
camera.annotate_text = " Hello world "
sleep(5)
camera.stop_preview()