'''
Optimizer: Genetic Algorithm Optimization
Date created: 27th December 2017
Licence: Python Software Foundation License version 2
'''

import random
from copy import deepcopy


class OptimizerGA(object):
    '''
    Genetic algorithm (GA) optimizer class.

    This class takes an OptimizationTarget object (which represents an
    individual organism) and replicates it to the required population size
    and store them in population dictionary (where the keys represents the
    sample IDs). These sample IDs will be reused over generations; hence,
    have to take account of population count to be unique. Two functions
    needs to be defined - mutate (which mutates the chromosomes in
    population[ID].chromosomes and are bounded by population[ID].
    chromosomes_lower_bounds and population[ID].chromosomes_upper_bounds
    for lower and upper value boundaries respectively), and mate (which
    eliminates unfit organisms and mates fit organisms for the next
    generation). There is a defined set of mating and mutation methods
    pre-defined but these can be overrode. The run method performs GA
    optimization on the population.

    Chromosomes in this class is the state in OptimizationTarget object.
    '''
    def __init__(self, optTarget, population_size=10, max_generations=100):
        '''
        Constructor method.

        @param optTarget: object to optimize.
        @type optTarget: optimizer_genetic.OptimizationTarget object
        @param population_size: number of organisms in population (Default
        = 10).
        @type population_size: integer
        @param max_generations: maximum number of generations to optimize
        (Default = 10).
        @type max_generations: integer
        '''
        self.optTarget = optTarget
        self.generations = 0
        self.max_generations = int(max_generations)
        self.population_size = int(population_size)
        self.population = {}
        for i in range(self.population_size):
            self.population[i] = deepcopy(self.optTarget)
        self.mutateFunction = 'random'
        self.mutationRate = 0.1
        self.matingFunction = 'top50'
        self.bestOrganism = None
        self.bestOrganismGeneration = 0
        self.worstOrganism = None
        self.worstOrganismGeneration = 0
        self.verbose = 0
        self.reportFunction = None

    def setMutate(self, name='random'):
        '''
        Method to set mutation scheme. Allowable mutation schemes are:
            - random

        @param name: name of mutation scheme (Default = random).
        @type name: string
        '''
        availableMutates = ['random']
        if str(name) == 'random':
            self.mutateFunction = self._mutateRandom
        elif callable(name):
            self.mutateFunction = name
        else:
            self.mutateFunction = self._mutateRandom

    def setMate(self, name='top50fission'):
        '''
        Method to set mating scheme. Allowable mating schemes are:
            - none
            - top50fission
            - topfission

        @param name: name of mating scheme (Default = none).
        @type name: string
        '''
        availableMates = ['none', 'top50fission', 'topfission']
        if str(name) == 'none':
            self.mateFunction = self._mateNone
        elif str(name) == 'top50fission':
            self.mateFunction = self._mateTop50Fission
        elif str(name) == 'topfission':
            self.mateFunction = self._mateTopFission    
        elif callable(name):
            self.mateFunction = name
        else:
            self.mateFunction = 'top50fission'

    def _runReport(self, population):
        '''
        Private method - Default population report for each generation.
        '''
        popFitness = [population[k].fitnessScore for k in population.keys()]
        bestFitness = max(popFitness)
        averageFitness = sum(popFitness) / float(len(popFitness))
        print('Generation %s, Average Fitness: %.7f, Best Fitness: %.7f' % \
              (self.generations+1, averageFitness, bestFitness))
        if int(self.verbose) > 2:
            print('Organism Fitness Scores: ' + str(popFitness))

    def run(self):
        '''
        Method to run the GA optimizer, which will execute the following steps
        until one of the organism is fitted (OptimizationTarget.fitted == True)
        or the maximum generation is reached:
            - for each organism, execute runnerFunction()
            - for each organism, execute dataFunction()
            - for each organism, execute comparatorFunction()
            - if none of the organisms is fitted, execute mutate function and
            mate function

        However, all organisms in the population will undergo mutation before
        the first execution. This is to prevent all organisms from getting the
        same fitness score at the first generation as all organisms are clones
        of each other at instantiation.

        @return: (generation count, population dictionary)
        '''

        if self.generations == 0:
            self.population = self.mutateFunction(self.population)
        while (self.generations < self.max_generations):
            for i in range(len(self.population)):
                self.population[i].runnerFunction()
                self.population[i].dataFunction()
                self.population[i].comparatorFunction()
            if self.reportFunction == None:
                self._runReport(self.population)
            else:
                self.reportFunction(self.generations, self.population)
            self._saveExtremes()
            if True in [self.population[i].fitted
                        for i in range(len(self.population))]:
                return (self.generation, self.population)
            self.population = self.mutateFunction(self.population)
            self.population = self.mateFunction(self.population)
            for i in range(len(self.population)):
                self.population[i].modifierFunction()
            self.generations = self.generations + 1

    def _saveExtremes(self):
        '''
        Private method - saves the best organism (organism with the highest
        fitness score) and worst organism (organism with the lowest fitness
        score) across generations.
        '''
        if self.bestOrganism == None:
            self.bestOrganism = self.population[0]
            self.bestOrganismGeneration = self.generations
        if self.worstOrganism == None:
            self.worstOrganism = self.population[0]
            self.worstOrganismGeneration = self.generations
        for k in self.population:
            if self.population[k].fitnessScore > self.bestOrganism.fitnessScore:
                self.bestOrganism = self.population[k]
                self.bestOrganismGeneration = self.generations
            if self.population[k].fitnessScore < self.worstOrganism.fitnessScore:
                self.worstOrganism = self.population[k]
                self.worstOrganismGeneration = self.generations

    def _mutateRandom(self, population):
        '''
        Private method - random mutation scheme (mutation scheme = random). 
        In this scheme, each of the chromosome is randomly mutated. A 
        random float (multiplier) between 0 and 2 will be generated for 
        each element on the chromosome. If the multiplier is lower than 
        1, then the data value of the element on the chromosome will be 
        reduced. if the multipler is more than 1, then the data value 
        of the element on the chromosome will be increased.

        @param population: population to mutate
        @type population: dictionary
        @return: mutated population
        '''
        def mutateChromosome(chr, lower, upper):
            position = range(len(chr))
            position = [random.choice(position)
                        for i in range(int(len(chr)*self.mutationRate))]
            for i in position:
                multiplier = random.randint(0, 2000) / float(1000)
                if multiplier < 1:
                    gap = chr[i] - lower[i]
                    chr[i] = chr[i] - (gap * multiplier)
                else:
                    multiplier = multiplier - 1
                    gap = upper[i] - chr[i]
                    chr[i] = chr[i] + (gap * multiplier)
            return chr
        def mutate(organism):
            for k in organism.states.keys():
                chr = organism.states[k]
                lower = organism.states_lower_bounds[k]
                upper = organism.states_upper_bounds[k]
                organism.states[k] = mutateChromosome(chr, lower, upper)
            return organism
        for k in population.keys():
            population[k] = mutate(population[k])
        return population

    def _mateNone(self, population):
        '''
        Private method - mating scheme which does nothing (mating scheme =
        top50fission). In this scheme, the original population is the new 
        population.

        @param population: population to mate
        @type population: dictionary
        @return: mated population
        '''
        return population

    def _mateTop50Fission(self, population):
        '''
        Private method - top 50% Fission mating scheme (mating scheme =
        top50fission). In this scheme, organisms with fitness score lower than
        the average fitness score of the population will be removed. The
        remaining organisms will be randomly selected for cloning / duplication
        to fill up the population.

        @param population: population to mate
        @type population: dictionary
        @return: mated population
        '''
        def kill(population):
            meanfitness = [population[k].fitnessScore
                           for k in self.population.keys()]
            meanfitness = sum(meanfitness) / len(meanfitness)
            setKill = []
            for k in self.population.keys():
                if population[k].fitnessScore < meanfitness:
                    setKill.append(k)
            if len(setKill) > (0.5*len(population)):
                setKill = [random.choice(setKill) 
                           for i in range(int(0.5*len(population)))]
                setKill = list(set(setKill))
            for k in setKill:
                del population[k]
            newpop = {}
            count = 0
            for k in self.population.keys():
                newpop[count] = population[k]
                count = count + 1
            return newpop
        def generate(population):
            fitOrg = list(population.keys())
            count = max(fitOrg)
            while len(population) < self.population_size:
                ID = random.choice(fitOrg)
                population[count] = deepcopy(population[ID])
                count = count + 1
            return population
        population = kill(population)
        population = generate(population)
        return population

    def _mateTopFission(self, population):
        '''
        Private method - top organism Fission mating scheme (mating scheme =
        topfission). In this scheme, only the organism with the best fitness
        score will survive and be cloned to fill up the population for the
        next generation.

        @param population: population to mate
        @type population: dictionary
        @return: mated population
        '''
        def kill(population):
            maxfitness = max([population[k].fitnessScore
                              for k in self.population.keys()])
            setKill = []
            for k in self.population.keys():
                if population[k].fitnessScore < maxfitness:
                    setKill.append(k)
            for k in setKill:
                del population[k]
            newpop = {}
            count = 0
            for k in self.population.keys():
                newpop[count] = population[k]
                count = count + 1
            return newpop
        def generate(population):
            fitOrg = list(population.keys())
            count = max(fitOrg)
            while len(population) < self.population_size:
                ID = random.choice(fitOrg)
                population[count] = deepcopy(population[ID])
                count = count + 1
            return population
        population = kill(population)
        population = generate(population)
        return population

