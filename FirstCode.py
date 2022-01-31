import time
from numpy.lib import math
import os
import pygame
import copy
import random
import numpy as np
pygame.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))


pointsmain = [[0, 600], [50, 600]]

screen = pygame.display.set_mode((1500, 1000))

def a(n1, t):
    new_point2 = []
    for i in range(len(n1)-1):
        vx = (-n1[i][0]+n1[i+1][0])
        vy = (-n1[i][1]+n1[i+1][1])
        new_point2.append((n1[i][0]+vx*t, n1[i][1]+vy*t))
    return new_point2

def c(pointsm):
    newpoints =[]
    carpos = 0
    passcar = 100
    nextpos = (0, 0)
    for pos in range(len(pointsm)-7):
        p = copy.copy(pointsm[pos:pos+6])

        for t in np.arange(0.4, 0.62, 0.02):

            n1 = copy.copy(p)

            for _ in range(len(p)-1):
                n1 = a(n1, t)

            newpoints += n1
            if passcar==10:
                nextpos = n1[0]
            if 385 < n1[0][0] < 415:
                carpos = n1[0][1]
                passcar = 0
            
            passcar+=1

            
    return newpoints, carpos, nextpos


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)

    newp = []
    for point in pointsmain:
        newp.append([point[0]-5, point[1]])
    pointsmain = copy.copy(newp)

    d = 0

    for point in pointsmain:

        if point[0] <-400:
            d = pointsmain.index(point)

        if point[0] < -700:
            pointsmain.remove(point)

    l = pointsmain[len(pointsmain)-1][0]
    if l < 2500:
        pointsmain.append((l+100, random.randint(300, 900)))

    newpoints, car, carnextpos = c(pointsmain[d:])
    vxcar = carnextpos[0]-400
    vycar = carnextpos[1]-car

    theta = math.acos(vxcar/math.sqrt(vxcar**2+vycar**2))
    if car < carnextpos[1]:
        theta *= -1
    print(theta)



    screen.fill((119, 181, 254))

    for i in range(len(newpoints)-1):
        pygame.draw.circle(screen, (200, 0, 0), (newpoints[i]), 3, width=0)

        #pygame.draw.polygon(screen, (133, 83, 15), ((newpoints[i]), (newpoints[i+1]), (newpoints[i+1][0], 1000), (newpoints[i][0], 1000)))

        #pygame.draw.polygon(screen, (0, 250, 0), ((newpoints[i]), (newpoints[i+1]), (newpoints[i+1][0], newpoints[i+1][1]+20), (newpoints[i][0], newpoints[i][1]+20)))

    pygame.draw.circle(screen, (255, 0, 0), (400, car), 5, width=0)
    pygame.draw.line(screen, (255, 0, 0), (400, car), (400+1*vxcar, car+1*vycar), width=4)


    pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(0, 0, 1500, 1000), width=10)


    pygame.display.flip()
            