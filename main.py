#############################################################
# 2D terrain generator using besier curve and random points #
#############################################################

import random
import pygame
import numpy as np
import time
        
pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
sizex, heightWindow = pygame.display.get_surface().get_size()

distanceBTpoints = 250

# M = np.array([[1, 0, 0, 0], [-3, 3, 0, 0], [3, -6, 3, 0], [-1, 3, -3, 1]])
    
class Curve:
    def __init__(self) -> None:
        self.FullCurve:list[CurvePart] = [] # list of all curve parts
        
        # points used to make the next part of the main curve, at each step the first point is removed will a new one is added
        self.mainPoints = [[distanceBTpoints*i, 500] for i in range(3)] 
    
    def bezierCurve(self, points):
        # 3 point Bezier curve generation
        # yield all points of the bezier curve has list [x, y]
        
        M = np.array([[0, 0, 1], [0, 2, -2], [1, -2, 1]])
        Mt = lambda x: np.array([1, x, x**2])
        
        return [(np.matmul(np.matmul(Mt(t), M), points)).astype(int) for t in np.arange(0, 1.02, 0.01)][::-1]
    
    def getCenter(self, p):
        np = [p[0]]
        for i in range(1, len(p)):
            x1, y1 = p[i-1]
            x2, y2 = p[i]
            np.append([x1 + (x2-x1)/2, y1 + (y2-y1)/2])   
            np.append(p[i]) 
        return np
        
    def addCurve(self):
        # update main points:
        self.mainPoints = [[0, self.mainPoints[1][1]], [distanceBTpoints, self.mainPoints[2][1]], [distanceBTpoints*2, random.randint(heightWindow//2, heightWindow - 150)]]
        
        # get new curve part with bezier
        curvePart = self.bezierCurve(np.array(self.getCenter(self.mainPoints)[1:-1]))
        
        # add the curve part to the full curve
        self.FullCurve.append(CurvePart(curvePart))

    def updateCurve(self):
        if not self.FullCurve or self.FullCurve[-1].posX <= sizex - distanceBTpoints :
            self.addCurve()
            
        if self.FullCurve[0].posX < -distanceBTpoints:
            self.FullCurve.pop(0)

class CurvePart:
    def __init__(self, points) -> None:
        self.posX = sizex -2
        self.surface = pygame.Surface((points[-1][0]-points[1][0] , heightWindow))
        self.create_surface(points)
        
    def create_surface(self, p):
        self.surface.fill((116, 208, 241))
        for i in range(len(p)-1):
            pygame.draw.rect(self.surface, (143, 89, 34), pygame.Rect(p[i][0]-125, p[i][1], p[i+1][0]-p[i][0], 1002))
            pygame.draw.rect(self.surface, (58, 200, 35), pygame.Rect(p[i][0]-125, p[i][1], p[i+1][0]-p[i][0], 30))
    
mainCurve = Curve()
while True:
    for event in pygame.event.get():
        if event.type == 256:
            exit()
            
    mainCurve.updateCurve()
    
    screen.fill((116, 0, 241))

    for curve in mainCurve.FullCurve:
        curve.posX -= 3
        screen.blit(curve.surface, (curve.posX, 0))
            
    pygame.display.flip()