'''
Example 16: Examining the natural effects of having no natural selection
schemes to the population whilst maintaining the same simulation parameters
as simulation 13's.

In this simulation,
    - 1 population of 100 organisms
    - each organism will have 1 chromosome of only 2 bases (1 and 0)
    - Deployed on just one eco-cell
    - 1% background point mutation on chromosome of 50 bases
    - no organism movement throughout the simulation
    - no Ragaraja interpretation of genome
    - 300 generations to be simulated
    - Fitness score goal of 50
'''

# needed to run this example without prior
# installation of DOSE into Python site-packages
try: 
	import run_examples_without_installation
except ImportError: pass

# Example codes starts from here
import dose, random
from collections import Counter
from copy import deepcopy

parameters = {
              "simulation_name": "example_15",
              "population_names": ['pop_01'],
              "population_locations": [[(0,0,0)]],
              "initial_chromosome": ['1','0'] * 250,
              "deployment_code": 1,
              "chromosome_bases": ['0','1'],
              "background_mutation": 0.01,
              "additional_mutation": 0.00,
              "mutation_type": 'point',
              "chromosome_size": 500,
              "genome_size": 1,
              "max_tape_length": 50,
              "clean_cell": True,
              "interpret_chromosome": False,
              "max_codon": 2000,
              "population_size": 100,
              "eco_cell_capacity": 0,
              "world_x": 1,
              "world_y": 1,
              "world_z": 1,
              "goal": 50,
              "maximum_generations": 5000,
              "fossilized_ratio": 0.01,
              "fossilized_frequency": 50,
              "print_frequency": 1,
              "ragaraja_version": 0,
              "ragaraja_instructions": ['000', '001', '010', 
                                        '011', '100', '101'],
              "eco_buried_frequency": 300,
              "database_file": "sim15_no_migration.db",
              "database_logging_frequency": 1
             }

class simulation_functions(dose.dose_functions):

    def organism_movement(self, Populations, pop_name, World): pass

    def organism_location(self, Populations, pop_name, World): pass

    def ecoregulate(self, World): pass

    def update_ecology(self, World, x, y, z): pass

    def update_local(self, World, x, y, z): pass

    def report(self, World): pass

    def fitness(self, Populations, pop_name):
        for organism in Populations[pop_name].agents:
            final_fitness = []
            chromosome = organism.genome[0].sequence
            zero_count = []
            for base_index in range(parameters["chromosome_size"] - 1):
                if int(chromosome[base_index]) == 0 and int(chromosome[base_index - 1]) != 0:
                    next_index = 1
                    while int(chromosome[next_index + base_index]) == 0:
                        next_index += 1
                        if (next_index + base_index) == parameters["chromosome_size"]: break
                    zero_count.append(next_index - 1)
            for sequence in range(len(zero_count)):
                if len(final_fitness) == 10: break
                seq_score = sorted(zero_count, reverse = True)[sequence]
                if seq_score > 5:
                    seq_score = 5
                final_fitness.append(seq_score)
            organism.status['fitness'] = sum(final_fitness)

    def mutation_scheme(self, organism):
        organism.genome[0].rmutate(parameters["mutation_type"],
                                   parameters["additional_mutation"])

    def prepopulation_control(self, Populations, pop_name): pass

    def mating(self, Populations, pop_name): 
        group = deepcopy(Populations[pop_name].agents)
        for organism in group:
            organism.generate_name()
            Populations[pop_name].agents.append(organism)

    def postpopulation_control(self, Populations, pop_name):
        group = deepcopy(Populations[pop_name].agents)
        for i in range(len(group)/2):
            Populations[pop_name].agents.remove(random.choice(Populations[pop_name].agents))

    def generation_events(self, Populations, pop_name): pass

    def population_report(self, Populations, pop_name):
        report_list = []
        for organism in Populations[pop_name].agents:
            chromosome = organism.status['identity']
            fitness = str(organism.status['fitness'])
            report_list.append(chromosome + ' ' + fitness)
        return '\n'.join(report_list)

    def database_report(self, con, cur, start_time, 
                        Populations, World, generation_count):
        try:
            dose.database_report_populations(con, cur, start_time, 
                                             Populations, generation_count)
        except: pass
        try:
            dose.database_report_world(con, cur, start_time, 
                                       World, generation_count)
        except: pass

    def deployment_scheme(self, Populations, pop_name, World): pass

dose.simulate(parameters, simulation_functions)