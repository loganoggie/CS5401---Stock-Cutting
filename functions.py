# functions for StockCutting.py

from re import findall
import os.path
import random
import re
from collections import defaultdict
from shapeClass import Shape

# determines and returns an appropriate filename for logs or solutions
def findFilename(filename):
    counter = 1
    while True:
        if os.path.isfile(filename):
            filename = re.sub(r'\d+', '', filename)
            filename = filename + str(counter)
            counter += 1
        else:
            break
    return filename

# loads the originalShapes list with the datapoints for each shape from rawShapes
# returns a list of all the shapes' data points
def InitializeDataPoints(rawShapes):
    originalShapes = [] # a list of the shapes - object contains x,y data points of each shape, starting at 0,0
    for directions in rawShapes:
        originalShapes.append(Shape.fromDirections(directions))
    return originalShapes


# function determines the maximum necessary length of the sheet
# returns the maximum length of fitness for all the shapes based on the length of the shapes (x values)
def MaxLength(originalShapes, sheetWidth):
    return sum([shape.findMaxDistance(sheetWidth) for shape in originalShapes])

# determines which genomes dominate other genomes
# returns a dict of keys (indexes  for each genome) and values (set of indexes of other genomes that dominate that indexed genome)
def FindDominance(tmpPopulation):
    dominatedBy = defaultdict(set)
    for i in range(len(tmpPopulation)):
        for genome in tmpPopulation:
            if (((tmpPopulation[i].lengthFitness > genome.lengthFitness) and (tmpPopulation[i].widthFitness >= genome.widthFitness)) or
                ((tmpPopulation[i].lengthFitness >= genome.lengthFitness) and (tmpPopulation[i].widthFitness > genome.widthFitness))):
                dominatedBy[genome].add(tmpPopulation[i])
    return dominatedBy

# creates a dominance table that assigns each genome a level
# returns a list of tuples, where each tuple includes a genome and its dominance level
def CreateDominanceTable(tmpPopulation):
    dominatedBy = FindDominance(tmpPopulation)
    dominanceTable = {}
    level = 0
    # pop = list(sorted(tmpPopulation, key=lambda g: len(dominatedBy[g])))
    # for index, genome in enumerate(pop):
        # print(index, list(sorted(map(lambda el: pop.index(el), dominatedBy[genome]))))
    while(len(dominanceTable) < len(tmpPopulation)):
        level -= 1
        placedGenomes = list(dominanceTable.keys())
        for genome in tmpPopulation:
            if genome not in dominanceTable and dominatedBy[genome].issubset(placedGenomes):
                dominanceTable[genome] = level
    return dominanceTable

# determines the two parents that will go into the gene crossover to produce offspring
# returns two parents
def ParentSelection(pSelection, parentPopulation, pkVal, fitness):
    if(pSelection == "rand"): # Unifrom Random Selection
        parent1 = parentPopulation[random.randint(0, len(parentPopulation)-1)]
        parent2 = parentPopulation[random.randint(0, len(parentPopulation)-1)]
    elif(pSelection == "fps"): # Fitness Proportional Selection
        parent1 = FitnessProportionalSelection(parentPopulation, fitness)
        parent2 = FitnessProportionalSelection(parentPopulation, fitness)
    elif(pSelection == "tournament"): # k-tournament selection with replacement
        parent1 = ParentTournamentSelection(parentPopulation, pkVal, fitness)
        parent2 = ParentTournamentSelection(parentPopulation, pkVal, fitness)
    else:
        raise NotImplementedError("parent selection type '{}' invalid:".format(pSelection))
    return parent1, parent2

# determines the population of survivors to move on as the future parent population
# returns the population of survivors
def SurvivalSelection(sSelection, strategy, mu, parentPopulation, offspringPopulation, skVal, fitness):
    if strategy == "plus":
        tmpPopulation = offspringPopulation + parentPopulation
    elif strategy == "comma":
        tmpPopulation = offspringPopulation

    survivalPopulation = set()
    if(sSelection == "rand"):
        while len(survivalPopulation) < mu:
            survivalPopulation.add(tmpPopulation[random.randint(0, len(tmpPopulation)-1)])
    elif(sSelection == "truncate"): # truncation
        survivalPopulation = sorted(tmpPopulation, key=fitness)[-mu:]
    elif(sSelection == "tournament"): # k-tournament selection without replacement
        survivalPopulation = SurvivorTournamentSelection(tmpPopulation, skVal, mu, fitness)
    elif(sSelection == "fps"):
        while len(survivalPopulation) < mu:
            survivalPopulation.add(FitnessProportionalSelection(tmpPopulation, fitness))
    else:
        raise NotImplementedError("survival selection type '{}' invalid:".format(sSelection))

    return list(survivalPopulation)

# function determines a parent using fitness proportional method
# returns a parent
def FitnessProportionalSelection(tmpPopulation, levelFitness):
    minFitness = min([levelFitness(genome) for genome in tmpPopulation])
    fitness = lambda genome: levelFitness(genome) - minFitness + 1
    fitnessSum = int(round(sum([fitness(genome) for genome in tmpPopulation])))
    pick = random.randint(0, fitnessSum - 1)
    val = 0
    for genome in tmpPopulation:
        val += fitness(genome)
        if val > pick:
            return genome
    raise ValueError("chose invalid fitness in FitnessProportionalSelection")

# function runs a k-tournament style selection WITH replacement to find a parent
# returns a parent
def ParentTournamentSelection(parentPopulation, pkVal, fitness):
    tournamentPopulation = set()
    while len(tournamentPopulation) < pkVal:
        tournamentPopulation.add(parentPopulation[random.randint(0, len(parentPopulation)-1)])
    return max(tournamentPopulation, key=fitness)

# function runs a k-tournament style selection WITHOUT replacement to find suriving offspring
# returns a lam-sized list of surivors
def SurvivorTournamentSelection(tmpPopulation, skVal, mu, fitness):
    survivalPopulation = set()
    while len(survivalPopulation) < mu:
        tournamentPopulation = set()
        while len(tournamentPopulation) <= skVal:
            tournamentPopulation.add(tmpPopulation[random.randint(0, len(tmpPopulation)-1)])
        survivalPopulation.add(max(tournamentPopulation, key=fitness))
    survivalPopulation = sorted(survivalPopulation, key=fitness)
    return list(survivalPopulation)

# random number generator that has a target value in between the high bound and low bound
def biasedRandom(lBound, hBound, target, steps=2):
    target = min(max(target, lBound), hBound)
    tmp = random.randint(lBound, hBound)
    for i in range(steps):
        tmp += round(random.random() * (target - tmp))
    return tmp

# function that outputs data to the solution file
# returns nothing
def WriteToSolutionFile(solutionFilename, overallBestSolutions):
    with open(solutionFilename, 'w') as solution:
        numSolutions = len(overallBestSolutions)
        solution.write(str(numSolutions))
        solution.write("\n\n")
        for genome in overallBestSolutions.values():
            for shape in genome.genes:
                solution.write(str(shape.origin[0]))
                solution.write(",")
                solution.write(str(shape.origin[1]))
                solution.write(",")
                solution.write(str(shape.rotation))
                solution.write("\n")
            solution.write("\n")

# the following functions are used for writing to the log
# the following functions return nothing
def StartLog(log_filename, instance_filename, seedVal):
    global log
    log = open(log_filename, 'w') # log.write(" ")
    log.write("Result Log\n\n")
    log.write("Probelm instance:  ")
    log.write(str(instance_filename))
    log.write("\n")
    log.write("Seed value:  ")
    log.write(str(seedVal))
    log.write("\n")

def RandomLog(runs, evaluations):
    log.write("Number of runs:  ")
    log.write(str(runs))
    log.write("\n")
    log.write("Number of evaluations:  ")
    log.write(str(evaluations))
    log.write("\n")

def EALog(mu, lam, pSelection, pkVal, sSelection, skVal, mRate, termination, nValue, strategy, penaltyCoefficient, adaptiveFlag):
    log.write("Size of parent population (mu):  ")
    log.write(str(mu))
    log.write("\n")
    log.write("Size of offspring population (lam):  ")
    log.write(str(lam))
    log.write("\n")
    log.write("Parent Selection parameter:  ")
    log.write(str(pSelection))
    log.write("\n")
    if pSelection == "tournament":
        log.write("k value for Parent Selection tournament:  ")
        log.write(str(pkVal))
        log.write("\n")
    log.write("Survival Selection parameter:  ")
    log.write(str(sSelection))
    log.write("\n")
    if sSelection == "tournament":
        log.write("k value for Survival Selection tournament:  ")
        log.write(str(skVal))
        log.write("\n")
    log.write("Mutation Rate:  ")
    log.write(str(mRate))
    log.write("\n")
    log.write("termination paramter:  ")
    log.write(str(termination))
    log.write("\n")
    log.write("n-value for termination type:  ")
    log.write(str(nValue))
    log.write("\n")
    log.write("Evolutionary Strategy Type:  ")
    log.write(str(strategy))
    log.write("\n")
    log.write("Penalty Coefficient:  ")
    log.write(str(penaltyCoefficient))
    log.write("\n")
    log.write("Self Adaptive Flag:  ")
    log.write(str(adaptiveFlag))
    log.write("\n\n<evals> <average first objective subfitness> <best first objective subfitness> <average second objective subfitness> <best second objective fitness>\n")

def NewRunLog(i):
    log.write("\n")
    log.write("Run ")
    log.write(str(i+1))
    log.write("\n")

def NewBestRandomFitnessLog(numEvals, bestFitnessScore):
    log.write(str(numEvals))
    log.write("\t")
    log.write(str(bestFitnessScore))
    log.write("\n")

def NewEAFitnessLog(numEvals, avgLengthFitness, bestLengthFitness, avgWidthFitness, bestWidthFitness):
    log.write(str(numEvals))
    log.write("\t")
    log.write(str(avgLengthFitness))
    log.write("\t")
    log.write(str(bestLengthFitness))
    log.write("\t")
    log.write(str(avgWidthFitness))
    log.write("\t")
    log.write(str(bestWidthFitness))
    log.write("\n")

def NewAdaptiveFitnessLog(numEvals, avgLengthFitness, bestLengthFitness, avgWidthFitness, bestWidthFitness, mRate):
    log.write(str(numEvals))
    log.write("\t")
    log.write(str(mRate))
    log.write("\t")
    log.write(str(avgLengthFitness))
    log.write("\t")
    log.write(str(bestLengthFitness))
    log.write("\t")
    log.write(str(avgWidthFitness))
    log.write("\t")
    log.write(str(bestWidthFitness))
    log.write("\n")

def CloseLog():
    log.close()
