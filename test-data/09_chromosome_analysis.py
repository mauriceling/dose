import sys, os, random
cwd = os.getcwd().split(os.sep)
cwd[-1] = 'dose'
cwd = os.sep.join(cwd)
sys.path.append(cwd)

import analytics

def calc_average_distance(genomes):
    genetic_distance_list = []
    for genome in genomes:
        chromosome = genome[0].sequence
        random_chromosome = random.choice(genomes)[0].sequence
        genetic_distance_list.append(analytics.hamming_distance(random_chromosome, chromosome))
    return analytics.average(genetic_distance_list)

sim09_adjacent = analytics.Analysis("sim09_adjacent.db", "pop_01")
sim09_adjacent.analyze_status_group_genome_by_generation("09_adjacent_sim_within_cell_analysis.csv", 
                                                         calc_average_distance, "location", 
                                                         sim09_adjacent.get_locations_list(), 
                                                         {"Average":analytics.average, 
                                                          "STDEV":analytics.standard_deviation}, 
                                                          range(1, 1001))

sim09_long_migration = analytics.Analysis("sim09_long_migration.db", "pop_01")
sim09_long_migration.analyze_status_group_genome_by_generation("sim09_long_migration_within_cell_analysis.csv",
                                                               calc_average_distance, "location", 
                                                               sim09_long_migration.get_locations_list(),
                                                               {"Average":analytics.average,
                                                                "STDEV":analytics.standard_deviation}, 
                                                               range(1, 1001))

sim09_no_migration = analytics.Analysis("sim09_no_migration.db", "pop_01")
sim09_no_migration.analyze_status_group_genome_by_generation("sim09_no_migration_within_cell_analysis.csv",
                                                             calc_average_distance, "location", 
                                                             sim09_no_migration.get_locations_list(),
                                                             {"Average":analytics.average,
                                                              "STDEV":analytics.standard_deviation}, 
                                                             range(1, 1001))