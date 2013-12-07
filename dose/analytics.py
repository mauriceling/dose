'''
File containing support functions for analysis of simulation results.

Date created: 21st October 2013
'''

import math

def hamming_distance(sequence_1, sequence_2):
    ham_dis = 0
    if (len(sequence_1) == len(sequence_2)):
        for i in xrange(len(sequence_1)):
            if int(sequence_1[i]) != int(sequence_2[i]):
                ham_dis = ham_dis + 1
    return ham_dis

def standard_deviation(data):
    data_average = float(sum(data))/len(data)
    summation = 0;
    for genetic_distance in data:
        summation += (genetic_distance - data_average) ** 2
    return math.sqrt(summation/(len(data) - 1))
