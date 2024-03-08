# -*- coding: utf-8 -*-
import pygame
import sys
import math
import random
import heapq
import pyproj
from pyproj import Proj

#Setup
pygame.init()
width, height = 1386, 684
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Autonomous Ship Simulation")

def dijkstra(world,start,goal):
    rows=1386
    col=684
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
    visited= set()
    heap= [(0,start)]
    costs={start:0}
    camefrom={}
    while len(heap)>0:
        currentcost,currentloc=heapq.heappop(heap)
        if currentloc== goal:
            path=[]
            while currentloc in camefrom:
                path.insert(0,currentloc)
                currentloc=camefrom[currentloc]
            path.insert(0,start)
            return currentcost,path
        if currentloc in visited:
            continue
        visited.add(currentloc)
        for optionx,optiony in directions:
            newx=currentloc[0]+optionx
            newy=currentloc[1]+optiony
            if newx>=0 and rows > newx and col > newy and newy >=0:
                newloc=(newx,newy)
                if newloc not in visited:
                    newcost=currentcost+ world[newy][newx]
                    if newloc not in costs or costs[newloc]>newcost:
                        costs[newloc]=newcost
                        heapq.heappush(heap, (newcost,newloc))
                        camefrom[newloc]=currentloc
    return float('inf'),[]
                
    


class port():
    def __init__(self):
        self.importData()
        self.dataCleanup()
        self.nameList()
        self.testTransformation()
        
    def importData(self):
        geoData = open("GeoData.csv", "r")          
        geoData = geoData.read()                 
        geoData = geoData.splitlines()                 
        self.portData = []                               
        for n in range(len(geoData) - 1):               
            individualItem = geoData[n +1]
            itemList = individualItem.split(",")
            self.portData.append(itemList)
        
    def dataCleanup(self):
        for n in range(len(self.portData)):  
            for x in range(2):
                self.portData[n][x+1] = self.portData[n][x+1].replace("Â","")
       

    def nameList(self):
        self.portName = []
        for n in range(len(self.portData)):
            self.portName.append(self.portData[n][0])
 
    def testTransformation(self):
        p = Proj(proj='robin',ellps='WGS84', preserve_units=True)
        x = []
        y = []
        for n in range(len(self.portData)):
            x.append(0)
            y.append(0)
            scaledXCoord = []
            scaledYCoord = []
        for n in range(len(self.portData)):
            indexX = self.portData[n][2].rfind("°") 
            minuteX = int(self.portData[n][2][indexX + 1:indexX + 3])
            degreeX = int(self.portData[n][2][1:indexX])
            testX = "W" in self.portData[n][2]
            if testX == True:
                scaledXCoord.append(degreeX + (minuteX/60))
            else:
                scaledXCoord.append(float(-1*(degreeX + (minuteX/60))))
         
        for n in range(len(self.portData)):
            indexY = self.portData[n][1].rfind("°")
            degreeY = int(self.portData[n][1][1:indexY])
            minuteY = int(self.portData[n][1][indexY + 1:indexY + 3])/60
            testY = "N" in self.portData[n][1]
            if testY == True:
                scaledYCoord.append(float(degreeY + minuteY))
            else:
                scaledYCoord.append(float(-1*(degreeY + minuteY)))
         
         
        for n in range(len(self.portData)):
             x[n],y[n] = p(scaledXCoord[n], scaledYCoord[n])
     
       
        self.x2 = []
        self.y2 = []
        for n in range(len(x)):
            self.x2.append(595-((x[n]/30000000)*1386))
            self.y2.append(398-((y[n]/14650000)*684))
  
            
  
portList = port()    


#Colors
blue= (100, 190, 230)
red=(255, 0, 0)
green=(31,96,35)
gray=(128,128,128)
pink=(220,69,136)






#background
land = pygame.image.load("earth 2.png").convert_alpha()
screenUpdate = pygame.transform.scale(land, (width,height))
mask= pygame.mask.from_surface(screenUpdate)
masksurface=mask.to_surface()
landrect=screenUpdate.get_rect()

#Ship
class ship():
    def __init__(self,x,y,size,selfish,goal):
        self.x=x
        self.y=y
        self.size=size
        if size== "small":
            self.ship_height=7
            self.ship_width=7
            self.colour=red
        elif size== "medium":
            self.ship_height=12
            self.ship_width=12
            self.colour=pink
        elif size== "large":
             self.ship_height=15
             self.ship_width=15
             self.colour=gray
             
        self.item=pygame.Rect(x,y,self.ship_width,self.ship_height)
        self.totaltravelled=0
        self.collisions=0
        self.selfish=selfish
        self.goal=goal
        pygame.draw.rect(screen,self.colour,self.item)       
        


        
# Update

screen.fill(blue)
screen.blit(screenUpdate, (0, 0))

tiles = [[0 for i in range(width)] for i in range(height)]

for y in range(height):
    for x in range(width):
        if screen.get_at((x, y)) == blue:
            tiles[y][x] = 1
        else:
            tiles[y][x] = 10000000000000000000





ships = [
    ship(0, 0, "medium", True, (1199, 699)),
    ship(0, 0, "small", True, (1199,699)),
    #ship(30, 70, "large", False, (800,320))
]               

def moveship(ships):
    paths = []
    originalgoal=[]
    for ship in ships:
        cost,path = dijkstra(tiles, (ship.x, ship.y), ship.goal)
        print(path)
        print(cost)
        paths.append(path)
        originalgoal.append(ship.goal)
    while (paths for path in paths):
        screen.fill(blue)
        screen.blit(screenUpdate, (0, 0))
        for j, ship in enumerate(ships):
            if len(paths[j])>0:
                (prevx, prevy) = (ship.x, ship.y)
                (ship.x,ship.y) = paths[j][0]
                ship.totaltravelled+=math.sqrt(((ship.x - prevx) ** 2) + ((ship.y - prevy) ** 2))
                ship.item = pygame.Rect(ship.x, ship.y, ship.ship_width, ship.ship_height)
                pygame.draw.rect(screen, ship.colour, ship.item)
                if ship.size=="large":
                    paths[j] = paths[j][1:]
                elif ship.size=="medium":
                    paths[j] = paths[j][2:]
                else:paths[j] = paths[j][3:]

                    
                
                for othership in ships:
                    if othership != ship and ship.item.colliderect(othership.item) and not ship.selfish:
                        ship.collisions+=1
                        newgoal = (ship.x+random.randint(-20, 20),ship.y +random.randint(-20, 20))
                        cost, newpath = dijkstra(tiles, (ship.x, ship.y), newgoal)
                        print(newpath)
                        ship.goal = newgoal
                        paths[j] = newpath
                        ship.selfish=True
                # If the ship has reached its original goal after avoiding the collision, restore the original goal
                if ship.goal == (ship.x, ship.y) and ship.goal != originalgoal[j]:
                    ship.goal = originalgoal[j]
                    cost, newpath = dijkstra(tiles, (ship.x, ship.y), ship.goal)
                    print(newpath)
                    paths[j] = newpath
                    ship.selfish=False
                    
                else: continue
        pygame.display.flip()
        pygame.time.delay(350)
    screen.fill(blue)
    screen.blit(screenUpdate, (0, 0))
    pygame.display.flip()
    


    
moveship(ships)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
