import sys, os, random
print 'Adding dose to working directory...'
cwd = os.getcwd().split(os.sep)
cwd[-1] = 'dose'
cwd = os.sep.join(cwd)
sys.path.append(cwd)

import analytics
import database_calls

database_filename = "sim10_adjacent.db"
outputfile = 'sim10_adjacent_within_cell_analysis.csv'
print 'Opening outputfile: ' + outputfile + '...'
outputfile = open(outputfile, 'w')
print 'Assembling database file directory...'
dbpath = os.getcwd().split(os.sep)
dbpath[-1] = 'examples'
dbpath = os.sep.join(dbpath)
dbpath = os.sep.join([dbpath, 'Simulations', database_filename])
print 'Connecting to database file: ' + database_filename + '...'
(con, cur) = database_calls.connect_database(dbpath, None)
print 'Acquiring simulation starting time...'
starting_time = database_calls.db_list_simulations(cur)[0][0]

print 'Constructing locations list...'
locations = []
for x in xrange(5):
    for y in xrange(5):
            locations.append((x,y,0));

def get_chromosomes_by_location(starting_time, pop_name, generation):
    organisms = database_calls.db_reconstruct_organisms(cur, starting_time, pop_name, generation)
    organism_chromosomes = {}
    for location in locations:
        organism_chromosomes[location] = []
        for organism in organisms:
            if organism.status['location'] == location:
                organism_chromosomes[location].append(organism.genome[0].sequence)
    return organism_chromosomes

print 'Writing outputfile header...'
header = [str(locations[i]).replace(", ","-") for i in xrange(len(locations))]
header = ['Generation'] + header
outputfile.write(','.join(header) + '\n')

print 'Starting main analysis...\n'
for generation in range(1, 1001):
    chromo_db = get_chromosomes_by_location(starting_time, 'pop_01', generation)
    result = [str(generation)]
    for location in locations:
        genetic_distance_list = []
        for chromosome in chromo_db[location]:
            random_chromosome = random.choice(chromo_db[location])
            genetic_distance_list.append(analytics.hamming_distance(random_chromosome, chromosome))
        average_distance = float(sum(genetic_distance_list))/len(genetic_distance_list)
        result.append(str(average_distance))
    outputfile.write(','.join(result) + '\n')    
    print 'Generation ' + str(generation) + ' analysis complete...',
    print '\r',

print '\nAnalysis complete!'