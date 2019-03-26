'''
Example 22: This is almost identical to Simulation 01 - most basic 
simulation (using default simulation functions) - but Ragaraja 
interpretation of genome.

In this simulation,
    - 1 population of 1 organisms
    - each organism will have 1 chromosome of only 4 bases (1, 2, 3, 4)
    - entire population will be deployed in one eco-cell (0, 0, 0)
    - 10% background point mutation on chromosome of 30 bases
    - no organism movement throughout the simulation
    - each base is mapped onto a Ragaraja instruction by user-defined 
    function
    - Ragaraja interpretation of genome (without new blood option)
    - 100 generations to be simulated
'''
# needed to run this example without prior
# installation of DOSE into Python site-packages
try: 
	import run_examples_without_installation
except ImportError: pass

# Example codes starts from here
import dose


def base_converter(source):
    converted = []
    for x in source:
        if x == '1': converted.append('000')
        elif x  == '2': converted.append('004')
        elif x  == '3': converted.append('008')
        elif x  == '4': converted.append('011')
        else: converted.append('200') # Jump identifier I
    return ''.join(converted)

parameters = {# Part 1: Simulation metadata
              "simulation_name": "22_simulation_01_with_interpretation",
              "population_names": ['pop_01'],

              # Part 2: World settings
              "world_x": 5,
              "world_y": 5,
              "world_z": 5,
              "population_locations": [[(0,0,0)]],
              "eco_cell_capacity": 100,
              "deployment_code": 1,

              # Part 3: Population settings
              "population_size": 1,

              # Part 4: Genetics settings
              "genome_size": 1,
              "chromosome_size": 300,
              "chromosome_bases": ['1', '2', '3', '4'],
              "initial_chromosome": ['1', '2', '3', '4'] * 75,

              # Part 5: Mutation settings
              "background_mutation": 0.1,
              "additional_mutation": 0,
              "mutation_type": 'point',
              
              # Part 6: Metabolic settings
              "interpreter": 'Ragaraja',
              "ragaraja_version": 66,
              "base_converter": base_converter,
              "ragaraja_instructions": ['000', '004', '008', '011'],
              "max_tape_length": 50,
              "interpret_chromosome": True,
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

    def fitness(self, Populations, pop_name): pass

    def mutation_scheme(self, organism): 
        organism.genome[0].rmutate(parameters["mutation_type"],
                                   parameters["additional_mutation"])

    def prepopulation_control(self, Populations, pop_name): pass

    def mating(self, Populations, pop_name): pass

    def postpopulation_control(self, Populations, pop_name): pass

    def generation_events(self, Populations, pop_name): pass

    def population_report(self, Populations, pop_name):
        sequences = [''.join(org.genome[0].sequence) for org in Populations[pop_name].agents]
        identities = [org.status['identity'] for org in Populations[pop_name].agents]
        locations = [str(org.status['location']) for org in Populations[pop_name].agents]
        demes = [org.status['deme'] for org in Populations[pop_name].agents]
        print(sequences)
        print([org.status['blood'] for org in Populations[pop_name].agents])
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
