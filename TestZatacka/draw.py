'''
Created on Apr 24, 2013

@author: Coco
'''
import random, pygame, sys, subprocess, time
from pygame.locals import *
from particle import *

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
BGCOLOR = SMOKE

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
class Draw():
    def __init__(self, player):
        global FPSCLOCK, DISPLAYSURF, BASICFONT
        global neighborCoords
        neighborCoords = []
        global neighborColors
        neighborColors = []
        global rectangles
        rectangles = []
        global particles
        particles = []
        
        self.player = player
        print 'enter draw'
        print self.player.getName()
        
        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        DISPLAYSURF.fill(BGCOLOR)
        BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
        pygame.display.set_caption('Zatacka')
        global img
        self.startGame()
        img = pygame.image.load('fog.jpg')
        pygame.time.wait(2000)
    
        while True:
            self.runGame()

    def startGame(self):
        myCoords = [{'x':self.player.node.head.x, 'y': self.player.node.head.y}]
        neighborStarts = []
        myColor = GREEN
        for n in self.player.node.neighbors.keys():
            neighborStarts.append({'x': self.player.node.neighbors[n].head.x, 'y': self.player.node.neighbors[n].head.y})
            neighborColors.append(RED)
#            
#        neighborStarts = [{'x': 55, 'y':55},{'x': 60, 'y': 65},{'x': 75, 'y': 40}]
#        neighborColors.append(RED)
#        neighborColors.append(PURPLE)
#        neighborColors.append(BLUE)
        numOfNeighbors = len(neighborStarts)
        for i in range(0, numOfNeighbors):
            print i
            print neighborStarts[i]
            neighborCoords.append([neighborStarts[i]])
        DISPLAYSURF.fill(BGCOLOR)
        self.initializeCloud()
    #    drawGrid()
    #    drawPixel(DISPLAYSURF, myColor, (myCoords[0]['x'],myCoords[0]['y']))
        print 'myCoords: ', myCoords[0]['x'], myCoords[0]['y']
        self.drawStartPoint(myCoords, myColor)
        
        for i in range(0, numOfNeighbors):
    #        drawPixel(DISPLAYSURF, neighborColors[i], (neighborCoords[i][0]['x'], neighborCoords[i][0]['y']))
            self.drawStartPoint(neighborCoords[i], neighborColors[i])
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    
    def runGame(self):
        # Start pos of players
        myCoords = [{'x':10, 'y': 20}]
        direction = 2  #RIGHT
    
        while True: # main game loop
            self.moveCloud()
            self.clearFog()
            for event in pygame.event.get(): # event handling loop
                print direction
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYDOWN:
                    if (event.key == K_LEFT or event.key == K_a):
                        direction = (direction + 7) % 8
                        self.player.node.direction = direction
#                        last_x += 2
#                        last_y += 1
                    elif (event.key == K_RIGHT or event.key == K_d):
                        direction = (direction + 1) % 8
                        self.player.node.direction = direction
#                        last_x += 1
#                        last_y += 2
                    elif event.key == K_ESCAPE:
                        self.terminate()
    #        drawGrid()
            color = GREEN
#            myCoords.append({'x': last_x, 'y': last_y})
            self.drawTrack(self.player.node.track, color)
            # draw neighbor
    #        print neighborCoords
    #        for i in range(0, numOfNeighbors):
    #            drawTrack(neighborCoords[i], neighborColors[i])
            for i in range(0, numOfNeighbors):
    #        drawPixel(DISPLAYSURF, neighborColors[i], (neighborCoords[i][0]['x'], neighborCoords[i][0]['y']))
                self.drawStartPoint(neighborCoords[i], neighborColors[i])
            
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    
    def terminate(self):
        pygame.quit()
        sys.exit()
    
    # draw lines from coords of a player
    def drawTrack(self, coords, color):
        points = []
        if len(coords) is 1:
            self.drawStartPoint(coords, color)
        else:
            for coord in coords:
                x = coord['x'] * CELLSIZE
                y = coord['y'] * CELLSIZE
                print 'track', x, y
                points.append((x, y))
            pygame.draw.lines(DISPLAYSURF, color, False, points, CELLSIZE)
    
    # draw a point
    def drawPixel(self, surface, color, pos):
        pygame.draw.line(surface, color, pos, pos)
    
    # draw start point with CELLSIZE specified
    def drawStartPoint(self, myCoords, color):
        for coord in myCoords:
            x = coord['x'] * CELLSIZE
            y = coord['y'] * CELLSIZE
            wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
            pygame.draw.rect(DISPLAYSURF, color, wormSegmentRect)
            wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
            pygame.draw.rect(DISPLAYSURF, color, wormInnerSegmentRect)
    
    # draw grid with CELLSIZE specified
    def drawGrid(self):
        for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
            pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
        for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
            pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))
    
    def clearFog(self):
        color = DARKGRAY
        rectangles = []
        for r in self.player.node.rectangles:
            rectangles.append(r)
        for n in self.player.node.neighbors.keys():
            for rec in self.player.node.neighbors[n].rectangles:
                rectangles.append(rec)
        reccount = 0
        for rectangle in rectangles:
            x = rectangle.tl.x
            y = rectangle.tl.y
            width = rectangle.br.x - rectangle.tl.x
            height = rectangle.br.y - rectangle.tl.y
            print reccount, 'x ', x, 'y ',y, 'w', width, 'h', height
            reccount += 1
            rect = pygame.Rect(x, y, width, height)
            DISPLAYSURF.fill(DARKGRAY, rect)
    
    def initializeCloud(self):
        particles.append( Particle(0, 0) )
        
    def moveCloud(self):
        for p in particles:
            p.move()
            DISPLAYSURF.blit(img, (p.x, p.y))
            