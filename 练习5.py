from turtle import *

fillcolor("yellow")
begin_fill()
while 1:
    forward(100)
    right(144)
    if abs(pos()) < 1:
            break
end_fill()
