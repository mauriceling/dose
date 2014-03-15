import sys, os, random
cwd = os.getcwd().split(os.sep)
cwd[-1] = 'dose'
cwd = os.sep.join(cwd)
sys.path.append(cwd)

import analytics

def analyze_fitness(fitness): return fitness

for sequence in xrange(5, 12):
    for trial in xrange(1, 4):
        analysis_name = "T" + str(trial) + "_" + str(sequence) + "x0_loss_1"
        sim14_analysis = analytics.Analysis(analysis_name + ".db", 
                                            "pop_01", starting_time = 'default')
        sim14_analysis.analyze_individual_status_by_generation(analysis_name + "_fitness_analysis.csv", 
                                                               "fitness", analyze_fitness, 
                                                               {"Average":analytics.average, 
                                                                "STDEV":analytics.standard_deviation}, 
                                                                xrange(201, 5201, 100))
