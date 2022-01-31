import random
from time import sleep
import pygame
from numpy import arange



pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
sizex, heightWindow = pygame.display.get_surface().get_size()
distanceBTpoints = 250

def getCenter(p):
    np = [p[0]]
    for i in range(1, len(p)):
        x1, y1 = p[i-1]
        x2, y2 = p[i]
        np.append([x1 + (x2-x1)/2, y1 + (y2-y1)/2])   
        np.append(p[i]) 
    return np
    
def bezier(n1, t):
    new_point = []
    for i in range(len(n1)-1):
        vx = (-n1[i][0]+n1[i+1][0])
        vy = (-n1[i][1]+n1[i+1][1])
        new_point.append((int(n1[i][0]+vx*t), int(n1[i][1]+vy*t)))
    return new_point
    
class Curve:
    def __init__(self) -> None:
        self.FullCurve = []
        self.mainPoints = [[distanceBTpoints*i, 500] for i in range(3)]

    def getAllPoints(self, p):
        newpoints =[]
        for t in arange(0, 1.02, 0.01):
            n1 = p
            for _ in range(len(p)-1):
                n1 = bezier(n1, t)
            newpoints += n1
        return newpoints

    def CreateNewCurvePart(self, points):
        Newpoints = points[1:-1]
        curve1 = self.getAllPoints(Newpoints)
        return curve1
        
    def addCurve(self):
        self.mainPoints = [[0, self.mainPoints[1][1]], [distanceBTpoints, self.mainPoints[2][1]], [distanceBTpoints*2, random.randint(heightWindow//2, heightWindow - 150)]]
        curvePart = self.CreateNewCurvePart(getCenter(self.mainPoints))
        newCP = CurvePart()
        newCP.points = curvePart
        self.FullCurve.append(newCP)

    def updateCurve(self):
        if not self.FullCurve or self.FullCurve[-1].posX <= sizex - distanceBTpoints :
            self.addCurve()
            
        if self.FullCurve[0].posX < -distanceBTpoints:
            self.FullCurve.pop(0)

class CurvePart:
    posX = sizex
    points = []
    
mainCurve = Curve()

while True:
    for event in pygame.event.get():
        if event.type == 256:
            exit()
            
    mainCurve.updateCurve()
    
    screen.fill((116, 208, 241))

    for curve in mainCurve.FullCurve:
        curve.posX -= 1
        for i in range(len(curve.points)-1):
            x = curve.points[i][0] + curve.posX - distanceBTpoints/2 
            pygame.draw.rect(screen, (143, 89, 34), pygame.Rect(x, curve.points[i][1], curve.points[i+1][0]-curve.points[i][0], 1002))
            pygame.draw.rect(screen, (58, 200, 35), pygame.Rect(x, curve.points[i][1], curve.points[i+1][0]-curve.points[i][0], 30))
            
    pygame.display.flip()
        
    
            
    
        
