
def importData():
    geoData = open("GeoData.csv", "r")
    tempString = geoData.read()
    templist1 = tempString.splitlines()
    tempLen1 = len(templist1)
    dataMap = {"Test" : 1234}
    for n in range(tempLen1 - 1):
        tempData1 = templist1[n +1]
        tempList2 = tempData1.split(",")
        tempString2 = tempList2[1] + "," + tempList2[2]
        dataMap[tempList2[0]] = tempString2
    del dataMap["Test"]
    return dataMap

print(importData())