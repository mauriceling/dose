'''
Example 28: Variations in 30 populations evolving without selection. 
Simulation code for Chew et al. 2020. Rapid Genetic Diversity with 
Variability between Replicated Digital Organism Simulations and its 
Implications on Cambrian Explosion. EC Clinical and Medical Case Reports 
3(11): 64-68.

In this simulation,
    - 1 population of 100 organisms
    - each organism will have 1 chromosome of only 4 bases (A, T, G, C)
    - each chromosome is 1200 bases
    - entire population will be deployed in one eco-cell (0, 0, 0)
    - 10% background point mutation on chromosome (PMID 14616055, 
    27185891)
    - no organism movement throughout the simulation
    - 2500 generations to be simulated
'''
# needed to run this example without prior
# installation of DOSE into Python site-packages
try: 
	import run_examples_without_installation
except ImportError: pass

import copy
import random

# Example codes starts from here
import dose

parameters = {# Part 1: Simulation metadata
              "simulation_name": "23_simulation_base",
              "population_names": ['pop_01'],

              # Part 2: World settings
              "world_x": 1,
              "world_y": 1,
              "world_z": 1,
              "population_locations": [[(0,0,0)]],
              "eco_cell_capacity": 1000,
              "deployment_code": 1,

              # Part 3: Population settings
              "population_size": 100,

              # Part 4: Genetics settings
              "genome_size": 1,
              "chromosome_size": 2000,
              "chromosome_bases": ['A', 'T', 'G', 'C'],
              "initial_chromosome": ['A', 'T', 'G', 'C'] * 300,

              # Part 5: Mutation settings
              "background_mutation": 0.1,
              "additional_mutation": 0,
              "mutation_type": 'point',
              
              # Part 6: Metabolic settings
              "interpreter": 'ragaraja',
              "instruction_size": 3,
              "ragaraja_version": 0,
              "base_converter": None,
              "ragaraja_instructions": [],
              "max_tape_length": 50,
              "interpret_chromosome": False,
              "clean_cell": False,
              "max_codon": 2000,

              # Part 7: Simulation settings
              "goal": 0,
              "maximum_generations": 2500,
              "eco_buried_frequency": 100,
              "fossilized_ratio": 0.01,
              "fossilized_frequency": 20,
              
              # Part 8: Simulation report settings
              "print_frequency": 10,
              "database_file": "simulation.db",
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
        pass

    def mutation_scheme(self, organism): 
        organism.genome[0].rmutate(parameters["mutation_type"],
                                   parameters["additional_mutation"])

    def prepopulation_control(self, Populations, pop_name): 
        pass

    def mating(self, Populations, pop_name):
        pass

    def postpopulation_control(self, Populations, pop_name): pass

    def generation_events(self, Populations, pop_name): pass

    def population_report(self, Populations, pop_name):
        agents = Populations[pop_name].agents
        sequences = [''.join(org.genome[0].sequence) for org in agents]
        identities = [org.status['identity'] for org in agents]
        gen_count = agents[0].status["generation"]
        for index in range(len(agents)):
            print('> %s|%s' % (str(gen_count), str(identities[index])))
            print(str(sequences[index]))

    def database_report(self, con, cur, start_time, 
                        Populations, World, generation_count):
        try: dose.database_report_populations(con, cur, start_time, 
                                    Populations, generation_count)
        except: pass
        try: dose.database_report_world(con, cur, start_time, 
                                        World, generation_count)
        except: pass

    def deployment_scheme(self, Populations, pop_name, World): pass

dose.simulate(parameters, simulation_functions)
