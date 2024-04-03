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
            if (i,j) in visitedPlots.keys():
                print("O", end="")
            else:
                print(plotGrid[i][j], end="")
        print("")
    print(sum)

#walk through grid and make list of visited spaces
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

solvepart1()