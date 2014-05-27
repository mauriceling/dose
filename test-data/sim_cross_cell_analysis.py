import sys, os, random
print('Adding dose to working directory...')
cwd = os.getcwd().split(os.sep)
cwd[-1] = 'dose'
cwd = os.sep.join(cwd)
sys.path.append(cwd)

import analytics
import database_calls

database_filename = "case_study_00.db"
outputfile = 'sim00_cross_cell_analysis.csv'
print('Opening outputfile: ' + outputfile + '...')
outputfile = open(outputfile, 'w')
print('Assembling database file directory...')
dbpath = os.getcwd().split(os.sep)
dbpath[-1] = 'examples'
dbpath = os.sep.join(dbpath)
dbpath = os.sep.join([dbpath, 'Simulations', database_filename])
print('Connecting to database file: ' + database_filename + '...')
(con, cur) = database_calls.connect_database(dbpath, None)
print('Acquiring simulation starting time...')
starting_time = database_calls.db_list_simulations(cur)[0][0]

print('Constructing locations list...')
locations = []
for x in xrange(5):
    for y in xrange(5):
            locations.append((x,y,0));

print('Writing outputfile header...')
header = ['Generation']
for location1 in locations:
    for location2 in locations:
        if location1 != location2:
            header.append(str(location1).replace(', ', '-') + ' vs ' + str(location2).replace(', ', '-'))
header = header + ['Average', 'Standard Deviaton']
outputfile.write(','.join(header) + '\n')

def get_chromosomes_by_location(starting_time, pop_name, generation):
    organisms = database_calls.db_reconstruct_organisms(cur, starting_time, pop_name, generation)
    organism_chromosomes = {}
    for location in locations:
        organism_chromosomes[location] = []
        for organism in organisms:
            if organism.status['location'] == location:
                organism_chromosomes[location].append(organism.genome[0].sequence)
    return organism_chromosomes

print('Starting main analysis...\n')
for generation in [1, 100, 200, 300, 400,500, 600, 700, 800, 900, 1000]:
    print('\rInitializing generation ' + str(generation) + '...')
    chromo_db = get_chromosomes_by_location(starting_time, 'pop_01', generation)
    results = [str(generation)]
    for location1 in locations:
        for location2 in locations:
            location_results = []
            if location1 != location2:
                print('\rAnalyzing ' + str(location1) + ' and ' + str(location2) + '...')
                for organism1 in chromo_db[location1]:
                    organism_results = []
                    for organism2 in chromo_db[location2]:
                        organism_results.append(analytics.hamming_distance(organism1, organism2))
                    location_results.append(analytics.average(organism_results))
                results.append(str(analytics.average(location_results)))
    outputfile.write(','.join(results) + '\n')
    print('\rGeneration ' + str(generation) + ' analysis complete...')

print('Simulation Anaysis Complete!')
