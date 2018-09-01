from operator import add

class SnakeCubePlacement (object):
    index = -1
    type = 0
    direction = (0, 0, 0)
    position = (-1, -1, -1)

    def __init__(self, index, type, direction, position):
        self.index = index
        self.type = type
        if (abs(direction[0]) + abs(direction[1]) + abs(direction[2])) != 1:
            raise "Invalid Direction"
        self.direction = direction
        self.position = position

    def getNextPosition(self):
        nextPosition = tuple(map(add, self.direction, self.position))
        return nextPosition

    def getNextPossibleDirections(self, direction):
        xArr = [(-1, 0, 0), (1, 0, 0)]
        yArr = [(0, -1, 0), (0, 1, 0)]
        zArr = [(0, 0, -1), (0, 0, 1)]
        if direction[0] is not 0:
            return yArr + zArr
        if direction[1] is not 0:
            return xArr + zArr
        if direction[2] is not 0:
            return xArr + yArr
        raise "hell"

    def getAvailableDirections(self):
        return [self.direction] if self.type == 0 else self.getNextPossibleDirections(self.direction)
    
    def __str__(self):
        return str(self.__class__) + '\n' + '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))


class SnakeCube (object):
    base = 3
    placements = []
    placementDefinitions = []

    def __init__(self, placementDefinitions):
        self.placementDefinitions = placementDefinitions
        
        length = len(placementDefinitions)
        if length != pow(self.base, self.base):
            raise "Bad length"
        self.buildCubeStart()

    def validBounds(self, position):
        if position[0] < 0 or position[0] > self.base - 1:
            return False
        if position[1] < 0 or position[1] > self.base - 1:
            return False
        if position[2] < 0 or position[2] > self.base - 1:
            return False
        return True

    def buildCubeStart(self):
        occupiedPlacements = [[[False for x in range(self.base)]for y in range(self.base)] for z in range(self.base)]
        startPosition = (0, 0, 0)
        occupiedPlacements[startPosition[0]][startPosition[1]][startPosition[2]] = True
        firstPlacement = SnakeCubePlacement(0, 0, (0, 0, 1), startPosition)
        self.placements = [firstPlacement]
        self.buildCube(0, occupiedPlacements)
        
    def buildCube(self, lastPlacementIndex, occupiedPlacements):
        lastPlacement = self.placements[lastPlacementIndex]
        currentIndex = lastPlacementIndex + 1
        currentPosition = lastPlacement.getNextPosition()
       
        if len(self.placementDefinitions) == currentIndex:
            return True
        if not self.validBounds(currentPosition):
            return False
        if occupiedPlacements[currentPosition[0]][currentPosition[1]][currentPosition[2]]:
            return False

        newPlacement = SnakeCubePlacement(
            currentIndex,
            self.placementDefinitions[currentIndex],
            lastPlacement.direction,
            currentPosition
        )

        possibleDirections = newPlacement.getAvailableDirections()
        for possibleDirection in possibleDirections:
            newPlacement.direction = possibleDirection
            occupiedPlacements[currentPosition[0]][currentPosition[1]][currentPosition[2]] = True
            self.placements.append(newPlacement)
            valid = self.buildCube(currentIndex, occupiedPlacements)
            occupiedPlacements[currentPosition[0]][currentPosition[1]][currentPosition[2]] = False
            if valid:
                return valid
            else:
                self.placements = self.placements[:-1]

        return False

    def printCube(self):
        for placement in self.placements:
            print(placement.index, placement.type,
                placement.direction, placement.position)

def buildSnakeCube():
    placementTypes = [0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0]
    snakeCube = SnakeCube(placementTypes)
    snakeCube.printCube()

if __name__ == '__main__':
    buildSnakeCube()
