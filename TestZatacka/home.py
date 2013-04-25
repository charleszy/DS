'''
Created on Apr 24, 2013

@author: Coco
'''
import pygame, pygbutton, sys
from pygame.locals import *
import platform
from draw import *
from printText import *
from game import *
from inputbox import *
import threading

numOfNeighbors = 0
FPS = 15
WINDOWWIDTH = 500
WINDOWHEIGHT = 500
CELLSIZE = 1
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BLUE      = ( 0,   0,  255)
PURPLE    = (160, 32,  240)
SMOKE     = (245, 245, 245)
YELLOW = (255, 255, 0) 
BGCOLOR = SMOKE

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYSURFACE.fill(WHITE)

    pygame.display.set_caption('Main Menu')

    buttonStart = pygbutton.PygButton((50, 50, 200, 30), 'Start')
    buttonReceive = pygbutton.PygButton((50, 100, 200, 30), 'Receive')

    vis = False
    count = 0
    timeleft = 10
    peerlist = []

    while True: # main game loop

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            event1 = buttonStart.handleEvent(event)
            event2 = buttonReceive.handleEvent(event)
            
            if 'click' in event1:
                pygame.time.wait(1000)
                print 'event1'
                vis = True
                p1.main_func("1")
                for msg in p1.peerlist:
                    peerlist.append(msg.name)

            if 'click' in event2:
                pygame.time.wait(1000)
                print 'event2'
                vis = True
                p1.main_func("2")
                for msg in p1.peerlist:
                    peerlist.append(msg.name)

        DISPLAYSURFACE.fill(WHITE)
        
        if vis is False:
            buttonStart.draw(DISPLAYSURFACE)
            buttonReceive.draw(DISPLAYSURFACE)

        else:
            pos = 0
            for peer in peerlist:
                printText(DISPLAYSURFACE, peer, "12", 30, 10, 10+30*pos, YELLOW)
                pos += 1
            printText(DISPLAYSURFACE, str(timeleft), "20", 50, 400, 400, BLUE)
            
            count += 1
            print count
            if count % FPS is 0:
                timeleft = 10 - count/FPS
            if count is 10*FPS:
                Draw(p1)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    global p1
    p1 = Player()
    name = name()
    p1.setName(name)
    main()
