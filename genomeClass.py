# genome class for StockCutting assignment

import random
from functions import biasedRandom
from collections import Counter

def GeneCrossover(parent1, parent2, selfAdaptive):
    index = 0
    offspring = []
    while index < len(parent1.genes):
        parentChoice = random.randint(1,2)
        if(parentChoice == 1):
            if(random.randint(1, 10000) <= parent1.mRate):
                mutatedShape = parent1.genes[index].fromMutate(parent1.sheetWidth, parent1.sheetLength)
                offspring.append(mutatedShape)
            else:
                offspring.append(parent1.genes[index])
            index += 1
        elif(parentChoice == 2):
            if(random.randint(1, 10000) <= parent2.mRate):
                mutatedShape = parent2.genes[index].fromMutate(parent2.sheetWidth, parent2.sheetLength)
                offspring.append(mutatedShape)
            else:
                offspring.append(parent2.genes[index])
            index += 1

    if random.randint(1,2) == 1:
        mRate = parent1.mRate
    else:
        mRate = parent2.mRate

    if selfAdaptive:
        if random.randint(1,10000) <= mRate+500: # always at least 5% chance of mutation rate
            mRate = biasedRandom(max(mRate-mRate//2, 0), min(mRate + mRate//2, 10000), mRate)

    return Genome(offspring, mRate, parent1.sheetWidth, parent1.sheetLength, parent1.penaltyCoefficient)


class Genome(object):
    def __init__(self, genes, mRate, sheetWidth, sheetLength, penaltyCoefficient):
        self.genes = genes
        self.mRate = mRate
        self.sheetWidth = sheetWidth
        self.sheetLength = sheetLength
        self.penaltyCoefficient = penaltyCoefficient
        self.paretoFrontLevel = None
        self._lengthFitness = None
        self._widthFitness = None

    def toValue(self):
        return tuple(map(lambda el: el.toValue(), self.genes))

    def fromRandom(self):
        shapes = []
        allPoints = set()
        for gene in self.genes:
            while True:
                newShape = gene.fromRandom(self.sheetWidth, self.sheetLength)
                if not allPoints.intersection(newShape.points):
                    break
            allPoints.update(newShape.points)
            shapes.append(newShape)
        genome = Genome(shapes, self.mRate, self.sheetWidth, self.sheetLength, self.penaltyCoefficient)
        return genome


    @property
    def genomeLength(self):
        xCoords = [x for shapeXs in [list(zip(*shape.points))[0] for shape in self.genes] for x in shapeXs]
        return max(xCoords)

    @property
    def genomeWidth(self):
        yCoords = [y for shapeYs in [list(zip(*shape.points))[1] for shape in self.genes] for y in shapeYs]
        return max(yCoords)

    def numOverlaps(self, shapeCount=-1): # CHECK VALIDITY
        if shapeCount < 0:
            shapeCount = len(self.genes)
        allPoints = Counter()
        for shape in self.genes[:shapeCount]:
            allPoints.update(shape.points)
        return sum([occurrences for point, occurrences in allPoints.items() if occurrences > 1])


    @property
    def lengthFitness(self):
        if self._lengthFitness is None:
            self._lengthFitness = self.sheetLength - self.genomeLength - (self.penaltyCoefficient * self.numOverlaps())
        return self._lengthFitness

    @property
    def widthFitness(self):
        if self._widthFitness is None:
            self._widthFitness = self.sheetWidth - self.genomeWidth - (self.penaltyCoefficient * self.numOverlaps())
            if self.widthFitness < 0:
                print(self.sheetWidth, "   ", self.genomeWidth)
        return self._widthFitness


    def Repair(self):
        index = 0
        for gene in self.genes:
            index += 1
            while self.numOverlaps(index):
                self.genes[index-1] = gene.fromMutate(self.sheetWidth, self.sheetLength)
