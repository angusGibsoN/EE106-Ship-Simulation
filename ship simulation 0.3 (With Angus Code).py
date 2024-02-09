import pygame
import sys

#Setup
pygame.init()
width, height = 1200, 700
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Autonomous Ship Simulation")
FPS = 60
clock = pygame.time.Clock()



def importData():                               ## defines Function called importData
    geoData = open("GeoData.csv", "r")          ## defines variable that contains the csv file in read mode
    tempString = geoData.read()                 ## defines a variable that contains a string of the raw data in the csv file
    templist1 = tempString.splitlines()         ## defines variable that is a list where each element is a string containing a line of the raw data
    tempLen1 = len(templist1)                   ## defines variable that is the number of elements in the list tempList1
    datalist = []                               ## defines empty list
    for n in range(tempLen1 - 1):               ## starts a for loop that has index n that increases from 0 by 1 each time until it reaches 1 less than tempLen1
        tempData1 = templist1[n +1]             ## defines varaiable that stoes data from the current(Nth + 1 term) element in tempList1
        tempList2 = tempData1.split(",")        ## defines a list where each element is a string that has been split by the comma form tempData1
        datalist.append(tempList2)              ## adds a new element to the list datalist where each new elemtn is a list in on of its self and is the current list in tempList2
    return datalist                             ## returns datalist after for loop is complete


def cleanUpData(portDataOld):                   ## defines funtion cleanUpData with data being passed in 
    newData = portDataOld                       ## defines variable newData that is the passed in data
    for n in range(len(portDataOld)):           ## starts for loop that has index n thats starts at 0 and increaes by 1 each loop until it reaches the number of elements - 1 in the newData
        for x in range(2):                      ## starts for loop where index x starts at 0 and increses to 1
            newData[n][x+1] = portDataOld[n][x+1].replace("Â","") ## replaces the character Â with nothing in the second and third element of each list within each element (That doesnt make sense)
    return newData                              ## returns new data


def convertXcoord(portData):
    for n in range(len(portData)):
        index = portData[n][2].rfind("°")
        xMinute = portData[n][2][index + 1:index + 3]
        degreeDecimal = int(xMinute)/60
        xDegrees = int(portData[n][2][1:index]) + degreeDecimal
        scaledCoord = (float(xDegrees)/180)*600
        test = "W" in portData[n][2]
        if test == True:
            xCoord = 520 - scaledCoord
        else:
            xCoord = 520 + scaledCoord
        portData[n][2] = xCoord
    return portData


portData = importData()                         ## calls the function importData and assigns its pass out into a variable
portData = cleanUpData(portData)
portData = convertXcoord(portData)

#Colors
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
pygame.display.flip()  
clock.tick(FPS)



if mask.overlap(ship_mask,((300,200))):
    print("true")
    

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
            
            
