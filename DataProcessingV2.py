# -*- coding: utf-8 -*-

def importData(): ## defines Function called importData
    geoData = open("GeoData.csv", "r") ## defines variable that contains the csv file in read mode
    tempString = geoData.read() ## defines a variable that contains a string of the raw data in the csv file
    templist1 = tempString.splitlines() ## defines variable that is a list where each element is a string containing a line of the raw data
    tempLen1 = len(templist1) ## defines variable that is the number of elements in the list tempList1
    datalist = [] ## defines empty list
    for n in range(tempLen1 - 1): ## starts a for loop that has index n that increases from 0 by 1 each time until it reaches 1 less than tempLen1
        tempData1 = templist1[n +1] ## defines varaiable that stoes data from the current(Nth + 1 term) element in tempList1
        tempList2 = tempData1.split(",") ## defines a list where each element is a string that has been split by the comma form tempData1
        datalist.append(tempList2) ## adds a new element to the list datalist where each new elemtn is a list in on of its self and is the current list in tempList2
    return datalist ## returns datalist after for loop is complete

def cleanUpData(portDataOld): ## defines funtion cleanUpData with data being passed in 
    newData = portDataOld ## defines variable newData that is the passed in data
    for n in range(len(portDataOld)): ## starts for loop that has index n thats starts at 0 and increaes by 1 each loop until it reaches the number of elements - 1 in the newData
        for x in range(2): ## starts for loop where index x starts at 0 and increses to 1
            newData[n][x+1] = portDataOld[n][x+1].replace("Â","") ## replaces the character Â with nothing in the second and third element of each list within each element (That doesnt make sense)
    return newData ## returns new data

portData = importData() ## calls the function importData and assigns its pass out into a variable
portData = cleanUpData(portData) ## calls the function cleanUpData and assings its output to a variable
