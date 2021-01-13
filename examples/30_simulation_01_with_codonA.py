'''
Example 31: This is almost identical to Simulation 01 - most basic 
simulation (using default simulation functions) - but CodonA 
interpretation of genome.

In this simulation,
    - 1 population of 1 organisms
    - each organism will have 1 chromosome of only 10 bases (1 to 0)
    - entire population will be deployed in one eco-cell (0, 0, 0)
    - the local_input of all all ecological cells is set to [1, 2, 3, 4]
    - 5% background point mutation on chromosome of 30 bases
    - no organism movement throughout the simulation
    - CodonA interpretation of genome on all instructions (with 
    new blood option)
    - 100 generations to be simulated
'''
# needed to run this example without prior
# installation of DOSE into Python site-packages
try: 
	import run_examples_without_installation
except ImportError: pass

# Example codes starts from here
import random
import dose


parameters = {# Part 1: Simulation metadata
              "simulation_name": "31_simulation_01_with_codonA",
              "population_names": ['pop_01'],

              # Part 2: World settings
              "world_x": 3,
              "world_y": 3,
              "world_z": 1,
              "population_locations": [[(0,0,0)]],
              "eco_cell_capacity": 100,
              "deployment_code": 1,

              # Part 3: Population settings
              "population_size": 1,

              # Part 4: Genetics settings
              "genome_size": 1,
              "chromosome_size": 300,
              "chromosome_bases": ['A', 'T', 'G', 'C'],
              "initial_chromosome": ['A', 'T', 'G', 'C'] * 75,

              # Part 5: Mutation settings
              "background_mutation": 0.05,
              "additional_mutation": 0,
              "mutation_type": 'point',
              
              # Part 6: Metabolic settings
              "interpreter": dose.codonA.interpreter,
              "instruction_size": 3,
              "ragaraja_version": "user-defined",
              "base_converter": None,
              "ragaraja_instructions": [],
              "max_tape_length": 4,
              "interpret_chromosome": True,
              "clean_cell": True,
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
        #print(sequences)
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

print('\n[' + parameters["simulation_name"].upper() + ' SIMULATION]')
print('Adding deployment scheme to simulation parameters...')
parameters["deployment_scheme"] = simulation_functions.deployment_scheme
print('Constructing World entity...')
World = dose.dose_world.World(parameters["world_x"],
                         parameters["world_y"],
                         parameters["world_z"])
dose.load_all_local_input(World, [1, 2, 3, 4])
print('Spawning populations...')
Populations = dose.spawn_populations(parameters)
print('\nStarting simulation on sequential ecological cell simulator...')
(simulation_functions, parameters, Populations, World) = \
    dose.sequential_simulator(simulation_functions, parameters, 
                              Populations, World)
print('\nSimulation ended...')
