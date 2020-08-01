#!/usr/bin/env python3

import pygame
import sys
import math
import random

class linea:
    def __init__(self, xInizio, yInizio, xFine, yFine, screen, color, weight, to):
        self.xInizio = xInizio
        self.xDir = xFine
        self.yInizio = yInizio
        self.yDir = yFine
        self.screen = screen
        self.color = color
        self.weight = weight
        self.To = to

    def draw(self):
        toX, toY =self.To
        pygame.draw.line(self.screen, self.color, (self.xInizio, self.yInizio), (toX, toY), self.weight)

    def collision(self, muro):
        x1 = muro.xInizio
        y1 = muro.yInizio
        x2 = muro.xFine
        y2 = muro.yFine

        x3 = self.xInizio
        y3 = self.yInizio
        x4 = self.xInizio + self.xDir
        y4 = self.yInizio + self.yDir

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return
        
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
        if t > 0 and t < 1 and u > 0:
            return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
        else:
            return

    def setTo(self, to):
        x, y = to

        self.To = (x, y)

    def setInit(self, x, y):
        self.xInizio = x
        self.yInizio = y

class Muro:
    def __init__(self, xInizio, yInizio, xFine, yFine, screen, color, weight):
        self.xInizio = xInizio
        self.xFine = xFine
        self.yInizio = yInizio
        self.yFine = yFine
        self.screen = screen
        self.color = color
        self.weight = weight

    def draw(self):
        pygame.draw.line(self.screen, self.color, (self.xInizio, self.yInizio), (self.xFine, self.yFine), self.weight)


def check(raggi, muri, screen, color):
    for r in raggi:
        minimum = (100000, 100000)
        for muro in muri:

            pt = r.collision(muro)
            if not pt is None and distance(minimum, (r.xInizio, r.yInizio)) > distance(pt, (r.xInizio, r.yInizio)):
                minimum = pt
        r.setTo(minimum)
            
def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)


def move(x, y, raggi):
    for r in raggi:
        r.setInit(x, y)



def Main():
    pygame.init()
    
    size = width, height = 800, 800
    centerX = int(width/2)
    centerY = int(height/2)
    x = centerX
    y = centerY
    font = pygame.font.SysFont("freesansbold.ttf", 50)
    screen = pygame.display.set_mode(size)
    black = 0, 0, 0
    red = 255, 0, 0
    white = 255, 255, 255
    raggio = int(5)
    muri=[]
    raggi=[]


    for i in range(0, 10):
        xInizio = random.randint(0, width - 150)
        yInizio = random.randint(0, height - 150)
        xFine = xInizio + random.randint(0, 150)  
        yFine = yInizio + random.randint(0, 150)

        muro = Muro(xInizio, yInizio, xFine, yFine, screen, red, 5)
        muri.append(muro)

    muri.append(Muro(0, 0, 0, height, screen, red, 5))
    muri.append(Muro(0, 0, width, 0, screen, red, 5))
    muri.append(Muro(width, 0, width, height, screen, red, 5))
    muri.append(Muro(0, height, width, height, screen, red, 5))

    for a in range(0, 360):
        xInizio = x
        yInizio = y
        xDir= math.cos(a)
        yDir = math.sin(a)

        r = linea(xInizio, yInizio, xDir, yDir, screen, white, 1, (0, 0))
        raggi.append(r)



    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()

            x, y = pygame.mouse.get_pos()
            move(x, y, raggi)
            
        screen.fill(black)
        for r in raggi:
            r.draw()

        for muro in muri:
            muro.draw()
            
        check(raggi, muri, screen, white)
        pygame.display.flip()


if __name__=="__main__":
    Main()