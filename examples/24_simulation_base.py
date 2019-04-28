'''
Example 24: This is a basic template for simulating the evolution of 
de novo origins of sequences.

In this simulation,
    - 1 population of 100 organisms
    - each organism will have 1 chromosome of only 4 bases (A, T, G, C)
    - entire population will be deployed in one eco-cell (0, 0, 0)
    - 10% background point mutation on chromosome of 30 bases
    - no organism movement throughout the simulation
    - fitness is calculated as minimum pairwise alignment of organism 
    chromosome to known sequences
    - 100 generations to be simulated
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

from Bio import Align
aligner = Align.PairwiseAligner()
aligner.mode = str('global')

known_sequences = ["ATAGCAGTAGCTAGTCGATGCTAGCTAG"]

parameters = {# Part 1: Simulation metadata
              "simulation_name": "23_simulation_base",
              "population_names": ['pop_01'],

              # Part 2: World settings
              "world_x": 1,
              "world_y": 1,
              "world_z": 1,
              "population_locations": [[(0,0,0)]],
              "eco_cell_capacity": 100,
              "deployment_code": 1,

              # Part 3: Population settings
              "population_size": 100,

              # Part 4: Genetics settings
              "genome_size": 1,
              "chromosome_size": 2000,
              "chromosome_bases": ['A', 'T', 'G', 'C'],
              "initial_chromosome": ['A', 'T', 'G', 'C'] * 25,

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
              "maximum_generations": 100,
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
      for index in range(len(Populations[pop_name].agents)):
        organism = Populations[pop_name].agents[index]
        chromosome = ''.join(organism.genome[0].sequence)
        score = min([aligner.score(chromosome, seq) 
                     for seq in known_sequences])
        Populations[pop_name].agents[index].status['fitness'] = score

    def mutation_scheme(self, organism): 
        organism.genome[0].rmutate(parameters["mutation_type"],
                                   parameters["additional_mutation"])

    def prepopulation_control(self, Populations, pop_name): pass

    def mating(self, Populations, pop_name):
      fitness = [org.status['fitness'] for org in Populations[pop_name].agents] 
      index = fitness.index(max(fitness))
      elimination = [x for x in range(parameters["population_size"]) 
                     if x != index]
      elimination = random.choice(elimination)
      replicated = copy.deepcopy(Populations[pop_name].agents[index])
      Populations[pop_name].agents[elimination] = replicated

    def postpopulation_control(self, Populations, pop_name): pass

    def generation_events(self, Populations, pop_name): pass

    def population_report(self, Populations, pop_name):
        sequences = [''.join(org.genome[0].sequence) for org in Populations[pop_name].agents]
        identities = [org.status['identity'] for org in Populations[pop_name].agents]
        locations = [str(org.status['location']) for org in Populations[pop_name].agents]
        demes = [org.status['deme'] for org in Populations[pop_name].agents]
        fitness = [org.status['fitness'] for org in Populations[pop_name].agents]
        print(fitness)
        print(max(fitness), sum(fitness)/len(fitness))
        return '\n'.join(sequences)

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
