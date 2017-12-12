# separates main from argeparse stuff

import random
import functions
from functions import CreateDominanceTable
from genomeClass import Genome, GeneCrossover
import shapeClass
from tqdm import tqdm

def Program(instanceFilename, log_filename, solution_filename, strategy, seed, evaluations, runs, mu, lam, pSelection,
                pkVal, sSelection, skVal, mRate, termination, nValue, penaltyCoefficient, adaptiveFlag, initialize):

    random.seed(seed) # initialize the random number generator

    rawShapes = [] # a list of the shape shift parameters

    # opens the file, acquires the first two parameters, then adds the shift parameters to rawShapes
    with open(instanceFilename) as inputFile:
        sheetWidth, numShapes = [int(x) for x in next(inputFile).split()]
        for line in inputFile.readlines():
            rawShapes.append(line.split())
    # create unused log/solution filenames
    logFilename = functions.findFilename(log_filename)
    solutionFilename = functions.findFilename(solution_filename)

    # fills the originalShapes list with shape datapoints and default rotation/origin values
    originalShapes = functions.InitializeDataPoints(rawShapes)

    # the maximum necessary length of the sheet
    sheetLength = functions.MaxLength(originalShapes, sheetWidth)

    originGenome = Genome(originalShapes, mRate, sheetWidth, sheetLength, penaltyCoefficient)

    # open and start the log file
    functions.StartLog(logFilename, instanceFilename, seed)

    overallBestRunSolutions = dict()


    if penaltyCoefficient:
        def CrossOver(parent1, parent2, mRate, sheetWidth, sheetLength):
            return GeneCrossover(parent1, parent2, adaptiveFlag)
    else:
        def CrossOver(parent1, parent2, mRate, sheetWidth, sheetLength):
            offspring = GeneCrossover(parent1, parent2, adaptiveFlag)
            offspring.Repair()
            return offspring

    functions.EALog(mu, lam, pSelection, pkVal, sSelection, skVal, mRate, termination, nValue, strategy, penaltyCoefficient, adaptiveFlag)

    for i in tqdm(range(int(runs)), unit='run', desc='Runs: ', dynamic_ncols=True):
        prevLevelOnes = None
        counter = 0

        if termination == 0: # terminates if number of evaluations is met
            def Terminate(numEvals, tmpPopulation):
                return numEvals >= evaluations
        elif termination == 1: # terminates if no change in top non-dominated level of population for n generations
            def Terminate(numEvals, tmpPopulation):
                nonlocal prevLevelOnes
                nonlocal counter

                if prevLevelOnes == None:
                    prevLevelOnes = set([genome.toValue() for genome, level in CreateDominanceTable(tmpPopulation).items() if level == -1])
                    return False

                currentLevelOnes = set([genome.toValue() for genome, level in CreateDominanceTable(tmpPopulation).items() if level == -1])

                if len(prevLevelOnes.union(currentLevelOnes)) == len(prevLevelOnes):
                    counter += 1
                else:
                    prevLevelOnes = currentLevelOnes
                    counter = 0
                if counter >= nValue:
                    return True
                else:
                    return False
        else:
            raise NotImplementedError("termination argument out of bounds: {}".format(termination))

        parentPopulation = []
        functions.NewRunLog(i)
        #print(originGenome.genes[11].points, "\n", originGenome.genes[13].points)
        # load the parentPopulation with valid solutions
        if initialize == "None":
            while len(parentPopulation) < mu:
                solution = originGenome.fromRandom()
                parentPopulation.append(solution)
        else:
            if os.path.isfile(solutionSeed):
                rawSolutionFile = []
                with open(solutionSeed) as inputFile:
                    for line in inputFile.readlines():
                        rawSolutionFile.append(line.split())
                numSeeds = int(rawSolutionFile[0])
                del rawSolutionFile[0]
                counter = 0
                while len(parentPopulation) <= numSeeds:
                    tmpShapes = []
                    for i in range(len(originalShapes)):
                        trans = rawSolutionFile[counter].split(",")
                        tmpShapes.append(Shape(originalShapes[i], trans[2], (trans[0], trans[1])))
                        counter += 1
                    parentPopulation.append(Genome(tmpShapes, mRate, sheetWidth, sheetLength, penaltyCoefficient))
                    tmpGenome = []
            else:
                raise ValueError("solution seed file is invalid")

            while len(parentPopulation) < mu:
                solution = originGenome.fromRandom()
                parentPopulation.append(solution)

        avgLengthFitness = sum(map(lambda el: el.lengthFitness, parentPopulation))/mu
        avgWidthFitness = sum(map(lambda el: el.widthFitness, parentPopulation))/mu

        offspringLevelTable = {}
        parentLevelTable = CreateDominanceTable(parentPopulation)
        def fitness(genome):

            if genome in offspringLevelTable:
                return offspringLevelTable[genome]
            elif genome in parentLevelTable:
                return parentLevelTable[genome]
            else:
                raise ValueError('Genome does not exist in Level Table: {}'.format(genome))

        mergeBest(overallBestRunSolutions, CreateDominanceTable(parentPopulation))

        bestParent = max(parentPopulation, key=fitness)

        index = 0
        numEvals = mu
        if adaptiveFlag:
            functions.NewAdaptiveFitnessLog(numEvals, round(avgLengthFitness, 3), bestParent.lengthFitness, round(avgWidthFitness, 3), bestParent.widthFitness, mRate)
        else:
            functions.NewEAFitnessLog(numEvals, round(avgLengthFitness, 3), bestParent.lengthFitness, round(avgWidthFitness, 3), bestParent.widthFitness)

        offspringPopulation = []
        with tqdm(total=evaluations, desc='Evals', unit='eval', leave=False, dynamic_ncols=True, unit_scale=True) as progress_bar:
            while not Terminate(numEvals, parentPopulation):
                while len(offspringPopulation) < lam:
                    parent1, parent2 = functions.ParentSelection(pSelection, parentPopulation, pkVal, fitness)
                    offspring = CrossOver(parent1, parent2, mRate, sheetWidth, sheetLength)
                    offspringPopulation.append(offspring)
                    progress_bar.update(1)
                offspringLevelTable = CreateDominanceTable(offspringPopulation)

                parentPopulation = functions.SurvivalSelection(sSelection, strategy, mu, parentPopulation, offspringPopulation, skVal, fitness)
                parentLevelTable = CreateDominanceTable(parentPopulation)

                mergeBest(overallBestRunSolutions, offspringLevelTable)
                mergeBest(overallBestRunSolutions, parentLevelTable)

                avgLenghtFitness = sum(map(lambda el: el.lengthFitness, parentPopulation))/mu
                avgWidthFitness = sum(map(lambda el: el.widthFitness, parentPopulation))/mu

                lengthFitness = sum(map(lambda g: g.lengthFitness, overallBestRunSolutions.values()))/len(overallBestRunSolutions)
                widthFitness = sum(map(lambda g: g.widthFitness, overallBestRunSolutions.values()))/len(overallBestRunSolutions)
                progress_bar.set_description('Evals ({},{})'.format(round(lengthFitness, 0), round(widthFitness, 0)))
                progress_bar.refresh()

                bestParent = max(parentPopulation, key=fitness)

                numEvals += lam

                if adaptiveFlag: # WILL NOT BE USED IN ASSIGNMENT 1D
                    avgmRate = sum(map(lambda el: el.mRate, parentPopulation))/mu
                    functions.NewAdaptiveFitnessLog(numEvals, round(avgLengthFitness, 3), bestParent.lengthFitness, round(avgWidthFitness, 3), bestParent.widthFitness, avgmRate)
                else:
                    functions.NewEAFitnessLog(numEvals, round(avgLengthFitness, 3), bestParent.lengthFitness, round(avgWidthFitness, 3), bestParent.widthFitness)

                offspringPopulation = []


    functions.WriteToSolutionFile(solutionFilename, overallBestRunSolutions)

    functions.CloseLog()

def mergeBest(bestSolutions, newLevelTable):
    newBestSolutions = dict([(genome.toValue(), genome) for genome, level in newLevelTable.items() if level == -1])
    bestSolutions.update(newBestSolutions)
    for genome, level in CreateDominanceTable(list(bestSolutions.values())).items():
        if level != -1:
            del bestSolutions[genome.toValue()]
