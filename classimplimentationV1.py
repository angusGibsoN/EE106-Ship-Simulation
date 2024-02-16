# -*- coding: utf-8 -*-
import random

        
        
class port():
    def __init__(self):
        self.importData()
        self.dataCleanup()
        self.convertXcoord()
        self.convertYcoord()
        self.nameList()
        
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
                
    def convertXcoord(self):
        self.xCoord = []
        for n in range(len(self.portData)):
            index = self.portData[n][2].rfind("°")
            scaledCoord = (float(int(self.portData[n][2][1:index]) + (int(self.portData[n][2][index + 1:index + 3])/60))/180)*600
            test = "W" in self.portData[n][2]
            if test == True:
                self.xCoord.append(520 - scaledCoord)
            else:
                self.xCoord.append(520 + scaledCoord)
            
    def convertYcoord(self):
        self.yCoord = []
        for n in range(len(self.portData)):
            index = self.portData[n][1].rfind("°")
            scaledCoord = (float(int(self.portData[n][1][1:index]) + (int(self.portData[n][1][index + 1:index + 3])/60))/90)*350
            test = "N" in self.portData[n][1]
            if test == True:
                self.yCoord.append(350 - scaledCoord)
            else:
                self.yCoord.append(350 + scaledCoord)
        
    def nameList(self):
        self.portName = []
        for n in range(len(self.portData)):
            self.portName.append(self.portData[n][0])
            
    def isPortFull(self, index):
        
        
      
class ship():
    def __init__(self):
        self.shipSpeed = self.setSpeed()
        self.shipCat = self.setCat()
        
    def setSpeed(self):
        speed = 5*random.randint(1,3)
        return speed
    
    def setCat(self):
        if self.shipSpeed > 10:
            cat = "L"
        elif self.shipSpeed < 10:
            cat = "S"
        else:
            cat = "M"
        return cat
            

portList = port()
print(portList.portName)

