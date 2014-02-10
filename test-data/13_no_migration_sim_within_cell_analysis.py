import sys, os, random
print 'Adding dose to working directory...'
cwd = os.getcwd().split(os.sep)
cwd[-1] = 'dose'
cwd = os.sep.join(cwd)
sys.path.append(cwd)

import analytics
import database_calls

database_filename = "T3_11x0.db"
outputfile = 'T3_11x0_analysis.csv'
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
locations = [(0,0,0)]

def get_fitness_by_generation(starting_time, pop_name, generation):
    organisms = database_calls.db_reconstruct_organisms(cur, starting_time, pop_name, generation)
    organism_fitness = []
    for organism in organisms:
        organism_fitness.append(organism.status['fitness'])
    return organism_fitness

print 'Writing outputfile header...'
header = [str(i) for i in xrange(1, 101)]
header = ['Generation'] + header + ['Average', 'Standard Error']
outputfile.write(','.join(header) + '\n')

print 'Starting main analysis...\n'
for generation in range(1, 301):
    fitness_list = get_fitness_by_generation(starting_time, 'pop_01', generation)
    result = [str(generation)]
    for fitness in fitness_list:
        result.append(str(fitness))
    result.append(str(analytics.average(fitness_list)))
    result.append(str(analytics.standard_deviation(fitness_list)))
    outputfile.write(','.join(result) + '\n')
    print 'Generation ' + str(generation) + ' analysis complete...',
    print '\r',

print '\nAnalysis complete!'