import sys, os, random
cwd = os.getcwd().split(os.sep)
cwd[-1] = 'dose'
cwd = os.sep.join(cwd)
sys.path.append(cwd)

import analytics

for sequence in xrange(5, 12):
    for trial in xrange(1, 4):
        analysis_name = "T" + str(trial) + "_" + str(sequence) + "x0_resistant_pool"
        resistant_pa = analytics.Analysis(analysis_name + ".db", "pop_01",
                                          starting_time = 'default')
        resistant_pa.analyze_status_group_count_by_generation(analysis_name + ".csv",
                                                              "fitness", 
                                                              resistant_pa.get_fitness_range_by_percentage(0.8),
                                                              None, generations = 'all')
        