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

    def updateCurve(self, n=1):
        for _ in range(n):

            if not self.FullCurve or self.FullCurve[-1].posX <= sizex - distanceBTpoints :
                self.addCurve()
                
            if self.FullCurve[0].posX < -distanceBTpoints:
                self.FullCurve.pop(0)

            for curve in self.FullCurve:
                curve.posX -= 3

class CurvePart:
    def __init__(self, points) -> None:
        self.posX = sizex -2 
        self.points = points
        print(points[-1][0]-points[1][0] )
        self.surface = pygame.Surface(((points[-1][0]-points[1][0]) , heightWindow))
        self.create_surface(points)
        
    def create_surface(self, p):
        self.surface.fill((116, 208, 241))
        for i in range(len(p)-1):
            pygame.draw.rect(self.surface, (143, 89, 34), pygame.Rect(p[i][0] - distanceBTpoints/2, p[i][1], p[i+1][0]-p[i][0], 1002))
            pygame.draw.rect(self.surface, (58, 200, 35), pygame.Rect(p[i][0] - distanceBTpoints/2, p[i][1], p[i+1][0]-p[i][0], 30))
    
class Car:
    def __init__(self) -> None:
        self.posCar = 400
        self.lengthCar = 100
        self.speed = 3

    def distbtPoints(self, a, b, c, d):
        return np.sqrt((a-c)**2+(b-d)**2)

    def draw(self, yposW1, vx, vy, boost):
        # get the perpendicular of the vector btw the two wheels
        x = vy
        y = -vx

        a = self.lengthCar / 125 # scale of the car

        BackWheel  = [self.posCar + x * a * 25, yposW1 + y * a * 25] # center pos of the back wheel
        FrontWheel = [self.posCar + x * a * 25 + self.lengthCar * vx , yposW1 + y * a * 25 + self.lengthCar * vy] # same, front wheel
        
        wheels = [BackWheel, FrontWheel]
        
        body    = [[self.posCar + (vx * p[0] + x * p[1]) * a, yposW1 + (vy * p[0] + y * p[1]) * a] for p in [[-30, 30], [-30, 100], [-20, 110], [90, 110], [135, 75], [160, 70], [160, 30]]]
        reactor = [[self.posCar + (vx * p[0] + x * p[1]) * a, yposW1 + (vy * p[0] + y * p[1]) * a] for p in [[-30, 42], [-45, 40], [-45, 90], [-30, 88]]]
        flame1  = [[self.posCar + (vx * p[0] + x * p[1]) * a, yposW1 + (vy * p[0] + y * p[1]) * a] for p in [[-45, 45], [-45, 85], [-100 ,90], [-55 ,72], [-120, 65], [-55, 58], [-100, 40]]]
        flame2  = [[self.posCar + (vx * p[0] + x * p[1]) * a, yposW1 + (vy * p[0] + y * p[1]) * a] for p in [[-45, 50], [-45, 80],  [-85 ,87], [-45 ,72], [-95, 65], [-45, 58], [-85, 43]]]
        
        car = [body, (200, 20, 20), reactor, (20, 20, 20)]
        flame = [flame1, (251, 163, 26), flame2, (255, 213, 0)]

        for i in range(0, len(car), 2):
            pygame.draw.polygon(screen, car[i+1], car[i])

        if boost:
            for i in range(0, len(flame), 2):
                pygame.draw.polygon(screen, flame[i+1], flame[i])

        pygame.draw.circle(screen, (30, 30, 30), wheels[0], self.lengthCar/5)
        pygame.draw.circle(screen, (30, 30, 30), wheels[1], self.lengthCar/5)
        

    def findPosCar(self, FullCurve):
        # get the y position of the back wheel and the inclination of the car

        # first we get the corresponding part of the mainCurve:
        for c in FullCurve:
            if c.posX - 3 < self.posCar and c.posX + 3 + distanceBTpoints > self.posCar:
                break

        # on this part of the curve, we find the closest point to the wheel
        smallOne = 3000
        yposW1 = 0

        for point in c.points:
            x, y = point
            d = abs(x +  c.posX - distanceBTpoints/2  - self.posCar)
            if d < smallOne:
                smallOne = d
                yposW1 = y
        # yposW1 is the height of the point of contact between the wheel and the road

        # then we get the position of the front wheel:
        indexCurvePart =  FullCurve.index(c)

        bestOne = 3000
        for c in FullCurve[indexCurvePart:indexCurvePart+2]: # for now, we consider that the frond wheel can only be on the two next part [should be changed]
            for point in c.points:
                x, y = point
                x += c.posX - distanceBTpoints/2 
                
                d = self.distbtPoints(x, y, self.posCar, yposW1)
                
                dist = abs(d - self.lengthCar)
                if dist < bestOne and x > self.posCar:
                    bestOne = dist
                    coordW2 = [x ,y]
        
        # unit vector between the two wheels   
        dist = self.distbtPoints(coordW2[0], coordW2[1], self.posCar, yposW1)     
        vx = (coordW2[0] - self.posCar) / dist
        vy = (coordW2[1] - yposW1) / dist

        return yposW1, vx, vy


def main():
    mainCurve = Curve()
    mainCurve.updateCurve(5000)
    car = Car()

    while True:

        key = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == 256  or key[pygame.K_ESCAPE]:
                exit()
                
        boost = key[pygame.K_SPACE]

        mainCurve.updateCurve(1 + boost*3)
        
        yposW1, vx, vy = car.findPosCar(mainCurve.FullCurve)
                
        screen.fill((116, 0, 241))

        for curve in mainCurve.FullCurve:
            
            screen.blit(curve.surface, (curve.posX, 0))
        
        car.draw(yposW1, vx, vy, boost)

        pygame.display.flip()


if __name__ == '__main__':
    main()