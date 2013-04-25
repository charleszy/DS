'''
Created on Apr 20, 2013

@author: Coco
'''
import pygame,random
from pygame.locals import *

xmax = 1000    #width of window
ymax = 600     #height of window

class Particle():
    def __init__(self, startx, starty):
        self.x = startx
        self.y = random.randint(0, starty)
        self.sx = startx
        self.sy = starty

    def move(self):
#        if self.y < 0:
#            self.x=self.sx
#            self.y=self.sy
#
#        else:
#            self.y-=1

        self.x+=random.randint(-4, 4)
