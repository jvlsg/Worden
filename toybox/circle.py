#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from drawille import Canvas, line, animate
import math

def circle(c,x0=0,y0=0,radius=0):
    for g in range(0,360,36):
        t = math.radians(g)
        x = x0 + math.cos(t) * radius
        y = y0 + math.sin(t) * radius
        c.set(x,y)
    print(c.frame(-20,-20,20,20))

if __name__ == "__main__":
    c = Canvas()
    c.set(0,-1)
    c.set(-1,0)
    c.set(0,0)
    c.set(0,1)
    c.set(1,0)
    circle(c,radius=6)
