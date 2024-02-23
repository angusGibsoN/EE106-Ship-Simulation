import pyproj
from pyproj import Proj

class port():
    def __init__(self):
        self.importData()
        self.dataCleanup()
        self.convertXcoord()
        self.convertYcoord()
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
                
    def convertXcoord(self):
        self.xCoord = []
        for n in range(len(self.portData)):
            index = self.portData[n][2].rfind("°")
            scaledCoord = (float(int(self.portData[n][2][1:index]) + (int(self.portData[n][2][index + 1:index + 3])/60)))
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
    
    def testTransformation(self):
        p = Proj(proj='robin',ellps='WGS84', preserve_units=False)
        x2 = []
        y2 = []
        for n in range(len(self.portData)):
            x,y = p(self.portData[n][2], self.portData[n][1])
            x2.append,y2.append  = p(x, y, inverse=True) # inverse transform
  
        
portList = port() 