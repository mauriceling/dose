'''
File containing support functions for analysis of simulation results.

Date created: 21st October 2013
'''

import math, sys, os, random, database_calls

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

class Analysis(object):

    def __init__(self, db_source, population_name, starting_time = 'default'):
        print '\n[INITIALIZING ANALYSIS]'
        self.db_source = db_source
        self.population_name = population_name
        print 'Assembling database file directory...'
        dbpath = os.getcwd().split(os.sep)
        dbpath[-1] = 'examples'
        dbpath = os.sep.join(dbpath)
        dbpath = os.sep.join([dbpath, 'Simulations', db_source])
        print 'Connecting to database file: ' + db_source + '...'
        (self.con, self.cur) = database_calls.connect_database(dbpath, None)
        print 'Acquiring simulation starting time...'
        if starting_time == 'default':
            self.starting_time = database_calls.db_list_simulations(self.cur)[0][0]
        else:
            self.starting_time = starting_time

    def get_locations_list(self):
        print 'Getting locations list...'
        world_x = database_calls.db_reconstruct_simulation_parameters(self.cur, self.starting_time)['world_x']
        world_y = database_calls.db_reconstruct_simulation_parameters(self.cur, self.starting_time)['world_y']
        world_z = database_calls.db_reconstruct_simulation_parameters(self.cur, self.starting_time)['world_z']
        return [(x,y,z) for x in xrange(world_x) for y in xrange(world_y) for z in xrange(world_z)]

    def get_fitness_range_by_percentage(self, percentage):
        print 'Getting fitness range...'
        fitness_goal = database_calls.db_reconstruct_simulation_parameters(self.cur, self.starting_time)['goal']
        return xrange(int(fitness_goal * percentage), fitness_goal + 1)

    def get_individual_status_list_by_generation(self, status, generation):
        status_dict = database_calls.db_get_organisms_status(self.cur, self.starting_time, self.population_name, status, [generation])
        status_list = status_dict[generation].values()
        return status_list

    def get_individual_genome_list_by_generation(self, generation):
        genome_dict = database_calls.db_get_organisms_genome(self.cur, self.starting_time, self.population_name, [generation])
        genome_list = genome_dict[generation].values()
        return genome_list

    def get_status_group_genome_by_generation(self, status, target_status, generation):
        organisms = database_calls.db_reconstruct_organisms(self.cur, self.starting_time, self.population_name, generation)
        genome_list = [organism.genome for organism in organisms if organism.status[status] == target_status]
        return genome_list

    def analyze_individual_status_by_generation(self, csv_output, status, status_analysis, aggregate_functions = None, generations = 'all'):
        print '\n[INDIVIDUAL ' + status.upper() + ' STATUS ANALYSIS]'
        print 'Opening outputfile: ' + csv_output + '...'
        outputfile = open(csv_output, 'w')
        print 'Getting population size...'
        pop_size = database_calls.db_reconstruct_simulation_parameters(self.cur, self.starting_time)['population_size']
        print 'Writing outputfile header...'
        header = ['Generation'] + [str(i) for i in xrange(1, pop_size + 1)]
        if aggregate_functions != None:
            header = header + [key for key in aggregate_functions.keys()]
        outputfile.write(','.join(header) + '\n')
        print 'Starting main analysis...'
        if generations == 'all':
            generation_list = database_calls.db_list_generations(self.cur, self.starting_time)
        else:
            generation_list = generations
        for generation in generation_list:
            print 'Analyzing generation ' + str(generation) + '...',
            print '\r',
            status_list = [status_analysis(stat) for stat in self.get_individual_status_list_by_generation(status, generation)]
            status_row = [str(generation)] + [str(stat_result) for stat_result in status_list]
            if aggregate_functions != None:
                for key in aggregate_functions.keys():
                    status_row.append(str(aggregate_functions[key](status_list)))
            outputfile.write(','.join(status_row) + '\n')
        print '\nIndividual [' + status + '] analysis complete!'
    
    def analyze_status_group_count_by_generation(self, csv_output, status, stats, aggregate_functions = None, generations = 'all'):
        print '\n[' + status.upper() + ' STATUS GROUP COUNT ANALYSIS]'
        print 'Opening outputfile: ' + csv_output + '...'
        outputfile = open(csv_output, 'w')
        print 'Constructing generations list...'
        if generations == 'all':
            generation_list = database_calls.db_list_generations(self.cur, self.starting_time)
        else:
            generation_list = generations
        print 'Writing outputfile header...'
        header = [str(stat).replace(", ","-") for stat in stats]
        if aggregate_functions == None:
            header = ['Generation'] + header
        else:
            header = ['Generation'] + header + [key for key in aggregate_functions.keys()]
        outputfile.write(','.join(header) + '\n')
        print 'Starting main analysis...'
        for generation in generation_list:
            print 'Analyzing generation ' + str(generation) + '...',
            print '\r',
            status_list = self.get_individual_status_list_by_generation(status, generation)
            status_row = [str(generation)] + [str(status_list.count(target_stat)) for target_stat in stats]
            if aggregate_functions != None:
                for key in aggregate_functions.keys():
                    status_row.append(str(aggregate_functions[key]([status_list.count(target_stat) for target_stat in stats])))
            outputfile.write(','.join(status_row) + '\n')    
        print '\nGrouped [' + status + '] count analysis complete!'

    def analyze_individual_genomes_by_generation(self, csv_output, genome_analysis, aggregate_functions = None, generations = 'all'):
        print '\n[INDIVIDUAL GENOME ANALYSIS]'
        print 'Opening outputfile: ' + csv_output + '...'
        outputfile = open(csv_output, 'w')
        print 'Getting population size...'
        pop_size = database_calls.db_reconstruct_simulation_parameters(self.cur, self.starting_time)['population_size']
        print 'Writing outputfile header...'
        header = ['Generation'] + [str(i) for i in xrange(1, pop_size + 1)]
        if aggregate_functions != None:
            header = header + [key for key in aggregate_functions.keys()]
        outputfile.write(','.join(header) + '\n')
        print 'Starting main analysis...'
        if generations == 'all':
            generation_list = database_calls.db_list_generations(self.cur, self.starting_time)
        else:
            generation_list = generations
        for generation in generation_list:
            print 'Analyzing generation ' + str(generation) + '...',
            print '\r',
            genome_list = [genome_analysis(genome) for genome in self.get_individual_genome_list_by_generation(generation)]
            status_row = [str(generation)] + [str(genome_result) for genome_result in genome_list]
            if aggregate_functions != None:
                for key in aggregate_functions.keys():
                    status_row.append(str(aggregate_functions[key](genome_list)))
            outputfile.write(','.join(status_row) + '\n')
        print '\nIndividual genome analysis complete!'

    def analyze_status_group_genome_by_generation(self, csv_output, genome_analysis, status, stats, aggregate_functions = None, generations = 'all'):
        print '\n[' + status.upper() + ' STATUS GROUP GENOME ANALYSIS]'
        print 'Opening outputfile: ' + csv_output + '...'
        outputfile = open(csv_output, 'w')
        print 'Constructing generations list...'
        if generations == 'all':
            generation_list = database_calls.db_list_generations(self.cur, self.starting_time)
        else:
            generation_list = generations
        print 'Writing outputfile header...'
        header = [str(stat).replace(", ","-") for stat in stats]
        if aggregate_functions == None:
            header = ['Generation'] + header
        else:
            header = ['Generation'] + header + [key for key in aggregate_functions.keys()]
        outputfile.write(','.join(header) + '\n')
        print 'Starting main analysis...'
        for generation in generation_list:
            print 'Analyzing generation ' + str(generation) + '...',
            print '\r',
            analyzed_genome_list = [genome_analysis(self.get_status_group_genome_by_generation(status, target_status, generation)) for target_status in stats]
            status_row = [str(generation)] + [str(status_result) for status_result in analyzed_genome_list]
            if aggregate_functions != None:
                for key in aggregate_functions.keys():
                    status_row.append(str(aggregate_functions[key](analyzed_genome_list)))
            outputfile.write(','.join(status_row) + '\n')    
        print '\nGrouped [' + status + '] genome analysis complete!'