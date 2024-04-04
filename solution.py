from textwrap import fill


directionsCoords = {
    "north": (-1,0),
    "south": (1,0),
    "west": (0,-1),
    "east": (0,1)
}

def solvepart1():
    #read in data
    data = fileRead("input.txt")
    global plotGrid
    plotGrid = []
    startPos = ()
    for i in range(len(data)):
        plotGrid.append(list(data[i].strip()))
        for j in range(len(plotGrid[i])):
            if plotGrid[i][j] == "S":
                startPos = (i,j)

    global visitedPlots
    visitedPlots = {}
    startPos = (0,len(plotGrid)-1)
    walk(startPos, 64)
    sum = 0

    validPos = []

    for pos in visitedPlots.keys():
        evenCol = False
        if ( abs(startPos[0] - pos[0]) % 2 == 0 ): evenCol = True
        evenRow = False
        if ( abs(startPos[1] - pos[1]) % 2 == 0 ): evenRow = True
        if ( evenCol == evenRow ): 
            sum += 1
            validPos.append(pos)
     
    for i in range(len(plotGrid)):
        for j in range(len(plotGrid[0])):
            if plotGrid[i][j] == "S":
                print("S", end="")
            elif (i,j) in visitedPlots:
                print("O", end="")
            else:
                print(plotGrid[i][j], end="")
        print("")

    print(sum)

#walk through grid breadth-first and make list of visited spaces
def walk(startPos, steps):
    queue = [(startPos, steps)]
    while len(queue) > 0:
        pos, remainingSteps = queue.pop(0)
        if (not inGrid(pos, plotGrid)) or (plotGrid[pos[0]][pos[1]] == "#"):
            continue

        if pos in visitedPlots.keys():
            if visitedPlots[pos] < remainingSteps:
                visitedPlots[pos] = remainingSteps
            else:
                continue
        else:
            visitedPlots[pos] = remainingSteps
        
        if remainingSteps == 0:
            continue

        for dir in directionsCoords.values():
            queue.append((posAdd(pos, dir), remainingSteps-1))

def solvepart2():
    #read in data
    data = fileRead("input.txt")
    global plotGrid
    plotGrid = []
    startPos = ()
    for i in range(len(data)):
        plotGrid.append(list(data[i].strip()))
        for j in range(len(plotGrid[i])):
            if plotGrid[i][j] == "S":
                startPos = (i,j)

    #need to calculate 13 possible areas
    #steps in area of filled map
    #steps in area of each of 4 corner slices
    #steps in area of each of 4 large corner slices
    #steps in are of each of 4 points
    allMaps = {
        "filled": ( startPos, 201 ), 
        "topLeftEmpty": ( (0,0), 64 ),
        "bottomLeftEmpty": ( (len(plotGrid)-1,0), 64 ),
        "topRightEmpty": ( (0,len(plotGrid)-1), 64 ),
        "bottomRightEmpty": ( (len(plotGrid)-1,len(plotGrid)-1), 64 ),
        "topLeftFull": ( (0,0), 195 ),
        "bottomLeftFull": ( (len(plotGrid)-1,0), 195 ),
        "topRightFull": ( (0,len(plotGrid)-1), 195 ),
        "bottomRightFull": ( (len(plotGrid)-1,len(plotGrid)-1), 195 ),
        "bottomPoint": ( (0, len(plotGrid) // 2), 130 ),
        "topPoint": ( (len(plotGrid)-1, len(plotGrid) // 2), 130 ),
        "leftPoint": ( (len(plotGrid) // 2, len(plotGrid)-1), 130 ),
        "rightPoint": ( (len(plotGrid) // 2, 0), 130 ),

    }
    allAreas = {}
    for name, start in allMaps.items():
        global visitedPlots
        visitedPlots = {}
        walk(start[0], start[1])
        filledAreaOdd = getEndingPointsInArea(visitedPlots.keys(), True)
        filledAreaEven = getEndingPointsInArea(visitedPlots.keys(), False)
        allAreas[name] = (filledAreaOdd, filledAreaEven)

    #caculate how many of each area should be added
    x = 26501365 // 131
    areaAmounts = {
        "filled": ( pow(x-1, 2 ), pow(x,2) ),
        "topLeftEmpty": (0, x),
        "bottomLeftEmpty": (0, x),
        "topRightEmpty": (0, x),
        "bottomRightEmpty": (0, x),
        "topLeftFull": (x - 1, 0),
        "bottomLeftFull": (x - 1, 0),
        "topRightFull": (x - 1, 0),
        "bottomRightFull": (x - 1, 0),
        "bottomPoint": (1, 0),
        "topPoint": (1, 0),
        "leftPoint": (1, 0),
        "rightPoint": (1, 0),

    }
    sum = 0
    for k,v in areaAmounts.items():
        for i in range(len(v)):
            sum = sum + (v[i] * allAreas[k][i])

    print(sum)



#checks all spaces in a list and sees which of them are valid ending spots, given an odd number of steps
def getEndingPointsInArea(visitedSpaces, odd):
    area = 0
    for pos in visitedSpaces:
        evenCol = False
        if ( pos[0] % 2 == 0 ): evenCol = True
        evenRow = False
        if ( pos[1] % 2 == 0 ): evenRow = True
        if odd:
            if ( evenCol != evenRow ): area += 1
        else:
            if ( evenCol == evenRow ): area += 1
    return area

#adds two coordinates together
def posAdd(pos1, pos2):
    return tuple([ sum(coords) for coords in zip(pos1, pos2) ])

#checks if a coordinate is in a grid
def inGrid(pos, grid):
    return pos[0] >= 0 and pos[0] < len(grid) and pos[1] >= 0 and pos[1] < len(grid[0])

def fileRead(name):
    data = []
    f = open(name, "r")
    for line in f:
        data.append(line);
    return data

solvepart2()