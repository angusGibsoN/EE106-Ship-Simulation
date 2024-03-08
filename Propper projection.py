# -*- coding: utf-8 -*-
import pygame
import sys
import pyproj
from pyproj import Proj

#Setup
pygame.init()
width, height = 1386, 684
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Autonomous Ship Simulation")
FPS = 60
clock = pygame.time.Clock()

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



blue= (100, 190, 230)
red=(255, 0, 0)
green=(31,96,35)

#Ship
def make_ship(ship_width,ship_height,x,y,speed):
    ship=pygame.draw.rect(screen, red, (x,y, ship_width, ship_height))
    return ship



#background
land = pygame.image.load("earth 2.png").convert_alpha()
screenUpdate = pygame.transform.scale(land, (width,height))
mask= pygame.mask.from_surface(screenUpdate)
masksurface=mask.to_surface()

     
#Update
screen.fill(blue)
screen.blit(screenUpdate,(0,0))
ship=make_ship(10,7,300,200,5)
ship_mask= pygame.mask.Mask((10,7))
ship_mask.fill()
for n in range(len(portList.portName)):
    pygame.draw.circle(screen,(255,0,144),(portList.x2[n],portList.y2[n]),4)
#pygame.draw.circle(screen,(0,0,255),(519.5,158.5),4)
pygame.display.flip()  
clock.tick(FPS)



if mask.overlap(ship_mask,((300,200))):
    print("true")
    

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
