import turtle as t
import math as m

screen = t.Screen()

for i in range(1000):
    vt = i
    x = (vt * 2) * m.cos(vt)
    y = (vt * 2) * m.sin(vt)
    t.goto(x, y)

screen.exitonclick()
