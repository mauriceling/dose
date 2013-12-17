'''
File containing support functions for analysis of simulation results.

Date created: 21st October 2013
'''

import math

def hamming_distance(sequence_1, sequence_2):
    return sum(ch1 != ch2 for ch1, ch2 in zip(sequence_1, sequence_2))

def standard_deviation(data):
    data_average = float(sum(data))/len(data)
    summation = 0;
    for genetic_distance in data:
        summation += (genetic_distance - data_average) ** 2
    return math.sqrt(summation/(len(data) - 1))

def average(data):
    return float(sum(data))/len(data)