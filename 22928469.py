"""
This program that can read the data from
a CSV (comma-separated values) file and return different interesting
analytical results.
Author: Khanh Hua Quang
Student ID: 22928469
"""

def main(inputFile,queryLocId,d1,d2):
    
    # open input file in read mode and append data into a list
    with open(inputFile, "r") as file:
        header = file.readline()[:-1].split(",")          
        temp = file.readlines()
        locationList = []
        for line in temp:
            locationList.append(line[:-1].split(","))

    # define column position in case of random header
    locIdPos, xPos, yPos, categoryPos = 0, 1, 2, 3
    headerPos = []
    for index in range(4):
        if header[index].lower() == "locid":
            headerPos.append(index)
    for index in range(4):
        if header[index].lower() == "latitude":
            headerPos.append(index)
    for index in range(4):
        if header[index].lower() == "longitude":
            headerPos.append(index)
    for index in range(4):
        if header[index].lower() == "category":
            headerPos.append(index)
    locIdPos = headerPos[0]
    xPos = headerPos[1]
    yPos = headerPos[2]
    categoryPos = headerPos[3]

    # compare the locId input with locId in locationList to add x, y, category element of that locId to a list
    def element(locId):
        outputList = []
        for location in locationList:
            if locId.lower() == location[locIdPos].lower():
                outputList.append(float(location[xPos]))
                outputList.append(float(location[yPos]))
                outputList.append(location[categoryPos].lower())
        return outputList

    # process raw parameters to handle exceptions
    x1 = element(queryLocId)[0]
    y1 = element(queryLocId)[1]
    mainCategory = element(queryLocId)[2]
    d1 = float(d1)
    d2 = float(d2)

    # define whether a specific location is in the area
    def isInArea(x1, x2, y1, y2, d1, d2):
        return x1 - d1 < x2 < x1 + d1 and y1 - d2 < y2 < y1 + d2

    # handle duplicated queryLocId and missing data
    def incorretedData(location):
        locId = location[locIdPos].strip().lower()
        x = location[xPos].strip().lower()
        y = location[yPos].strip().lower()
        category = location[categoryPos].strip().lower()
        return locId == queryLocId.lower() or locId[1:] == "" or locId == '' or x == '' or y == '' or category == '' or locId == "n/a"  or x == "n/a" or y == "n/a" or category == "n/a"

    # return locList list
    locList = []
    def locListFunc():
        locListStrip = []
        for location in locationList:
            if incorretedData(location):
                continue
            x2 = float(location[xPos])
            y2 = float(location[yPos])
            if isInArea(x1, x2, y1, y2, d1, d2):
                locList.append(location[locIdPos].upper()) 
        # output strip list
        for locId in locList:
            locListStrip.append(locId.strip())
        return locListStrip
        
    # return simLocList list
    simLocList = []
    def simLocListFunc():
        simLocListStrip = []
        for locId in locList:
            if element(locId)[2].lower().strip() == mainCategory:
                simLocList.append(locId)
        # output strip list
        for locId in simLocList:
            simLocListStrip.append(locId.strip())
        return simLocListStrip
    
    # return the distance to main location point
    def distanceFunc(x1, x2, y1, y2):
        distance = round(((((x2 - x1)**2) + (y2 - y1)**2)) ** (1/2), 4)
        return distance

    # return distSorted list
    distSorted = []
    def distSortedFunc():
        for locId in simLocList:
            x2  = element(locId)[0]
            y2  = element(locId)[1]
            distance = distanceFunc(x1, x2, y1, y2)
            distSorted.append(distance)
        return sorted(distSorted)

    # calculate the average
    def average(input):
        if input == 0 or len(input) == 0:
            return 0
        avg = round(sum(input) / len(input), 4)
        return avg

    # calculate the standard deviation
    def standardDeviation(input):
        if input == 0 or len(input) == 0:
            return 0
        accumulate = 0
        for element in input:
            accumulate += (element - average(input)) ** 2
        std = round((accumulate / len(input)) ** (1/2), 4)
        return std
    
    # return avgstd list
    avgstd = []
    def avgstdFunc():
        avg = average(distSorted)
        std = standardDeviation(distSorted)
        avgstd.append(avg)
        avgstd.append(std)
        return avgstd

    return locListFunc(), simLocListFunc(), distSortedFunc(), avgstdFunc()

# IMPORTANT: handle exeptions, also delete print(), main()
# NEED TO REMOVE 
locList, simLocList, distSorted, avgstd = main("/Users/khanhhuaquang/Documents/GitHub/CITS1401-Project/Locations-sample-Project1 copy.csv", "L83", "1.5", 2.2)
print(locList)
print(simLocList)
print(distSorted)
print(avgstd)
# NEED TO REMOVE