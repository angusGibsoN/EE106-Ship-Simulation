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
        self.coordTransformation()
        self.docked = [0] * len(self.portName)
        
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
 
    def coordTransformation(self):
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
            self.x2.append(int(595-((x[n]/30000000)*1386)))
            self.y2.append(int(398-((y[n]/14650000)*684)))
  
            
  
portlist = port()    



#Colors
blue= (100, 190, 230)
red=(255, 0, 0)
green=(31,96,35)
gray=(128,128,128)
pink=(220,69,136)
purple= (255,0,144)






#background
land = pygame.image.load("earth 2.png").convert_alpha()
screenUpdate = pygame.transform.scale(land, (width,height))
mask= pygame.mask.from_surface(screenUpdate)
masksurface=mask.to_surface()
landrect=screenUpdate.get_rect()

#Ship
class ship():
    def __init__(self,size,selfish):
        self.startLocation()
        self.size=size
        self.selfish=selfish
        self.assignSize()
        self.endLocation()
        self.item=pygame.Rect(x,y,self.ship_width,self.ship_height)
        self.totaltravelled=0
        self.collisions=0
        pygame.draw.rect(screen,self.colour,self.item)     
        
    def startLocation(self):
        p=random.randint(0, (len(portlist.portName))-1)
        self.x=portlist.x2[p]
        self.y=portlist.y2[p]
        
    def assignSize(self):
        if self.size== "small":
            self.ship_height=7
            self.ship_width=7
            self.colour=red
        elif self.size== "medium":
            self.ship_height=12
            self.ship_width=12
            self.colour=pink
        elif self.size== "large":
             self.ship_height=15
             self.ship_width=15
             self.colour=gray
        
    def endLocation(self):
        p=random.randint(0, (len(portlist.portName))-1)
        self.goal=(portlist.x2[p],portlist.y2[p])
        
    def isAlturistic(self,prevx,prevy,index):
        if self.selfish != True:
            bool = self.crashDetection(prevx,prevy,index)
        return bool
            
    def crashDetection(self,prevx,prevy,index):
        if index == 0:
            UP = [prevx,prevy]
            PUP = [prevx,prevy]
        UP = PUP
        PUP = [prevx,prevy]
        posVector = [PUP[0]-UP[0],PUP[1]-UP[1]]
        self.fieldCentre = [PUP[0]+2*posVector[0],PUP[1]+2*posVector[1]]
        detectionField = pygame.Rect(self.fieldCentre[0], self.fieldCentre[1], 10, 10)
        pygame.draw.rect(screen, blue, detectionField)
        for x in ships:
            collide = pygame.Rect.colliderect(detectionField, ships[x])
            if collide == True and x != index:
                crashCourse = True
        return crashCourse


        
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
    ship("medium", True),
    ship("small", True),
    ship("large", True),
    ship("small", True),
    ship("medium", True),
    ship("medium", True),
    ship("small", True),
    ship("small", True),
    ship("medium", True),
    ship("small", True),
    ship("medium", True),
    ship("medium", True),
    ship("small", True),
    ship("large", True),
    ]               

def moveship(ships):
    while True:
        paths = []
        
        # Initialize paths and original goals for each ship
        for ship in ships:
            if ship.goal == (ship.x, ship.y):
                randIndex = random.randint(0, len(portlist.portName) - 1)
                ship.goal = (portlist.x2[randIndex], portlist.y2[randIndex])
            cost, path = dijkstra(tiles, (ship.x, ship.y), ship.goal)
            paths.append(path)
        
        # Continue moving ships until all paths are empty
        while any(paths):
            screen.fill(blue)
            screen.blit(screenUpdate, (0, 0))
            for n in range(len(portlist.portName)):
                pygame.draw.circle(screen, purple, (portlist.x2[n], portlist.y2[n]), 4)
            for j, ship in enumerate(ships):
                if len(paths[j]) > 0:
                    (prevx, prevy) = (ship.x, ship.y)
                    (ship.x, ship.y) = paths[j][0]
                    ship.totaltravelled += math.sqrt(((ship.x - prevx) ** 2) + ((ship.y - prevy) ** 2))
                    ship.item = pygame.Rect(ship.x, ship.y, ship.ship_width, ship.ship_height)
                    pygame.draw.rect(screen, ship.colour, ship.item)
                    isCrash = ship.isAlturistic(prevx,prevy,j)
                    if isCrash == True:
                        if ship.size == "large":
                            paths[j] = paths[j][0:]
                        elif ship.size == "medium":
                            paths[j] = paths[j][0:]
                        else:
                            paths[j] = paths[j][0:]
                    else:
                        if ship.size == "large":
                            paths[j] = paths[j][1:]
                        elif ship.size == "medium":
                            paths[j] = paths[j][2:]
                        else:
                            paths[j] = paths[j][3:]
                    
                    # Check if the ship is attempting to dock at a port with more than 5 docks
                    for portindex, portcoords in enumerate(portlist.portName):
                        if (ship.x, ship.y) == (portlist.x2[portindex], portlist.y2[portindex]):
                            if portlist.docked[portindex] >= 5:
                                # If more than 5 docks are occupied, choose a new port
                                newportindex = random.choice([i for i in range(len(portlist.portName)) if portlist.docked[i] < 5])
                                ship.goal = (portlist.x2[newportindex], portlist.y2[newportindex])
                                cost, newpath = dijkstra(tiles, (ship.x, ship.y), ship.goal)
                                paths[j] = newpath
                                break
                            else:
                                # If there are less than 5 docks occupied, allow docking
                                portlist.docked[portindex] += 1
                                break
                    if not ship.selfish:
                        for k, other_ship in enumerate(ships):
                            if k != j and (other_ship.x, other_ship.y) == (ship.x, ship.y) and other_ship.goal == ship.goal:
                                paths[j] = paths[k]
                                break
            pygame.display.flip()
            pygame.time.delay(200)
        for ship in ships:
            randIndex = random.randint(0, len(portlist.portName) - 1)
            ship.goal = (portlist.x2[randIndex], portlist.y2[randIndex])

    




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            for ship in ships:
                print(ship)
                print("total collisions:",ship.collisions)
                print("total travelled:",ship.totaltravelled)
            pygame.quit()
            sys.exit()
    moveship(ships)
