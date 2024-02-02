# -*- coding: utf-8 -*-

def importData():
    geoData = open("GeoData.csv", "r")
    tempString = geoData.read()
    templist1 = tempString.splitlines()
    tempLen1 = len(templist1)
    datalist = []
    for n in range(tempLen1 - 1):
        tempData1 = templist1[n +1]
        tempList2 = tempData1.split(",")
        datalist.append(tempList2)
    return datalist

portData = importData()



def cleanUpData(portDataOld):
    newData = portDataOld
    for n in range(len(portDataOld)):
        for x in range(2):
            newData[n][x+1] = portDataOld[n][x+1].replace("Â","")
    return newData

portData = cleanUpData(portData)
    
