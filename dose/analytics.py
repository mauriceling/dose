'''
File containing support functions for analysis of simulation results.

Date created: 21st October 2013
'''

import math

def hamming_distance(sequence_1, sequence_2):
    '''
    Calculates Hamming distance of 2 string input.
    
    @param sequence_1: first input
    @type sequence_1: string
    @param sequence_2: second input
    @type sequence_2: string
    @return: Hamming distance in integer
    '''
    return sum(ch1 != ch2 for ch1, ch2 in zip(sequence_1, sequence_2))

def standard_deviation(data):
    '''
    Calculates standard deviation
    
    @param data: list of float or integer
    @return: standard deviation of data
    '''
    data_average = float(sum(data))/len(data)
    summation = 0
    for genetic_distance in data:
        summation = summation + ((genetic_distance - data_average) ** 2)
    return math.sqrt(summation/(len(data) - 1))

def average(data):
    '''
    Calculates arithmetic mean
    
    @param data: list of float or integer
    @return: arithmetic mean of data
    '''
    return float(sum(data))/len(data)