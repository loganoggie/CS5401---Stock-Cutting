# shape class for StockCutting assignment

import random
import functions

counter = 0
class Shape(object):
    @classmethod
    def fromDirections(cls, directions):
        global counter
        counter += 1
        rotation = 0
        origin = 0,0
        x, y = 0, 0
        points = set()
        points.add((x,y)) # temproary list used to store data points before adding to originalShapes
        for direction in directions:
            length = int(direction[1:])
            if 'U' in direction:
                for k in range(length):
                    y += 1
                    points.add((x,y))
            elif 'D' in direction:
                for k in range(length):
                    y -= 1
                    points.add((x,y))
            elif 'L' in direction:
                for k in range(length):
                    x -= 1
                    points.add((x,y))
            elif 'R' in direction:
                for k in range(length):
                    x += 1
                    points.add((x,y))
        return cls(points, rotation, origin)


    def __init__(self, points, rotation, origin):
        self.points = set(points)
        self.rotation = rotation
        self.origin = origin


    def toValue(self):
        return tuple(self.points)


    def fromTranslation(self, xShift, yShift): # was MoveShape
        movedPoints = set()
        for point in self.points:
            movedPoints.add((point[0]+xShift, point[1]+yShift))
        newOrigin = (self.origin[0] + xShift, self.origin[1] + yShift)
        return Shape(movedPoints, self.rotation, newOrigin)


    def fromRotation(self, rotation): # was RotateShape
        rotatedPoints = set()
        if rotation == 0: # no rotation
            rotatedPoints.update(self.points)
        elif rotation == 1: # 90 degree rotation - (x,y,0) to (y,−x,1)
            for point in self.points:
                rotatedPoints.add((point[1], point[0]*(-1)))
        elif rotation == 2: # 180 degree rotation - (x,y,0) to (−x,−y,2)
            for point in self.points:
                rotatedPoints.add((point[0]*(-1), point[1]*(-1)))
        elif rotation == 3: # 270 degree rotation - (x,y,0) to (−y, x,3)
            for point in self.points:
                rotatedPoints.add((point[1]*(-1), point[0]))
        else:
            raise NotImplementedError("rotation value out of bounds: {}".format(rotation))
        return Shape(rotatedPoints, (rotation+self.rotation)%4, self.origin)


    def fromRandom(self, sheetWidth, sheetLength):
        rotatedShape = self.fromTransformation(self.origin[0], self.origin[1], random.randint(0, 3))
        xMargin, yMargin = rotatedShape.getShapeMargins()
        newOrigin = functions.biasedRandom(xMargin[0], sheetLength - xMargin[1] - 1, rotatedShape.origin[0]//2), functions.biasedRandom(yMargin[0], sheetWidth - yMargin[1] - 1, rotatedShape.origin[1])
        return rotatedShape.fromTransformation(newOrigin[0], newOrigin[1], 0)


    def fromTransformation(self, xDest, yDest, rotation):
        return self.fromTranslation(-self.origin[0], -self.origin[1]).fromRotation(rotation).fromTranslation(xDest, yDest)


    def fromMutate(self, sheetWidth, sheetLength):
        rotatedShape = self.fromTransformation(self.origin[0], self.origin[1], random.randint(0, 3))
        xMargin, yMargin = rotatedShape.getShapeMargins()
        newOrigin = functions.biasedRandom(xMargin[0], sheetLength - xMargin[1] - 1, rotatedShape.origin[0]//2), functions.biasedRandom(yMargin[0], sheetWidth - yMargin[1] - 1, rotatedShape.origin[1])
        return rotatedShape.fromTransformation(newOrigin[0], newOrigin[1], 0)


    def findMaxDistance(self, sheetWidth):
        xCoords, yCoords = zip(*self.points)
        length = max(xCoords) - min(xCoords) + 1
        width = max(yCoords) - min(yCoords) + 1

        if max(length, width) <= sheetWidth:
            return max(length, width)
        else:
            return min(length, width)


    def getShapeMargins(self):
        xCoords, yCoords = zip(*self.points)
        xMargin = self.origin[0] - min(xCoords), max(xCoords) - self.origin[0]
        yMargin = self.origin[1] - min(yCoords), max(yCoords) - self.origin[1]
        return xMargin, yMargin
