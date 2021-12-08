'''
Optimizer: Optimization Target Class
Date created: 27th December 2017
Licence: Python Software Foundation License version 2
'''

import random
from copy import deepcopy

class OptimizationTarget(object):
    '''
    Abstract class to create the object to be optimized. This class
    is used to created an inherited class, which is the optimization
    target, where the states that are to be optimized.

    The way optimization executes is as follows: Firstly, The
    runnerFunction in the inherited class represents the method to
    execute the chromosomes to generate the executionResults. Secondly,
    the dataFunction in the inherited class represents the method to
    select required data variables (reduce the number of data variables)
    from executionResults into comparatorData. Finally, the
    comparatorFunction in the inherited class compares between the
    targetResults and comparatorData to generate a fitnessScore. The higher
    the fitness score, the fitter the organism and the higher chances it
    gets into the next generation.

    The states_lower_bound and states_upper_bound represents the lower 
    and upper bound values of the states, which can be used during 
    optimization.
    '''
    def __init__(self):
        '''
        Constructor method.
        '''
        self.states = {}
        self.states_lower_bounds = {}
        self.states_upper_bounds = {}
        self.targetResults = []
        self.executionResults = []
        self.comparatorData = []
        self.fitnessScore = 0
        self.fitted = False

    def dataFunction(self):
        '''
        Method to be inherited and represents the selection of
        self.executionResults into self.comparatorData. For example,
        self.executionResults may be a list of 100 elements but
        obnly 10 of the elements are experimentally known (self.
        targetResults) and matched. Hence, the format of self.
        comparatorData should be the same as self.targetResults.
        '''
        self.comparatorData = []

    def comparatorFunction(self):
        '''
        Method to be inherited and represent the fitness function,
        which compares self.comparatorData to self.targetResults
        and generate a fitness score (self.fitnessScore). This method
        must set self.fitted to True when the required organism
        achieves the required fitness score. The higher the fitness
        score, the fitter the organism and the higher chances it
        gets into the next generation.
        '''
        self.fitnessScore = 0

    def runnerFunction(self):
        '''
        Method to be inherited and represents the execution of the
        organism. This method must use self.chromosomes and the
        results to be fed into self.executionResults.
        '''
        pass

    def modifierFunction(self):
        '''
        Method to be inherited and represents a function to modify 
        the chromosomes (such as, changing the size of the chromosomes) 
        during execution.
        '''
        pass