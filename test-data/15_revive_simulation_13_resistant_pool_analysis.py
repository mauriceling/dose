import sys, os, random
print 'Adding dose to working directory...'
cwd = os.getcwd().split(os.sep)
cwd[-1] = 'dose'
cwd = os.sep.join(cwd)
sys.path.append(cwd)

import analytics
import database_calls

database_filename = "T3_11x0_revival.db"
outputfile = 'T3_11x0_revival_analysis.csv'
fitness_goal = 110
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
header = ['Generation']
resistant_range = range(int(fitness_goal * .8), fitness_goal + 1)
for i in resistant_range:
	header.append('FSCORE:' + str(i))
outputfile.write(','.join(header) + '\n')

print 'Starting main analysis...\n'
for generation in range(201, 5201):
	fitness_list = get_fitness_by_generation(starting_time, 'pop_01', generation)
	resistant_pool = {}
	for i in resistant_range:
		resistant_pool[i] = 0
		for fitness in fitness_list:
			if fitness == i:
				resistant_pool[i] += 1
	result = [str(generation)]
	for i in resistant_range:
		result.append(str(resistant_pool[i]))
	outputfile.write(','.join(result) + '\n')
	print 'Generation ' + str(generation) + ' analysis complete...',
	print '\r',

print '\nAnalysis complete!'