'''
Example 21: This is almost identical to Simulation 01 - most basic 
simulation (using default simulation functions) - but Ragaraja 
interpretation of genome (on all implemented Ragaraja instructions 
without new blood option)

In this simulation,
    - 1 population of 1 organisms
    - each organism will have 1 chromosome of only 4 bases (A, T, G, C)
    - entire population will be deployed in one eco-cell (0, 0, 0)
    - 10% background point mutation on chromosome of 30 bases
    - no organism movement throughout the simulation
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

parameters = {
              "simulation_name": "21_simulation_01_with_interpretation",
              "population_names": ['pop_01'],
              "population_locations": [[(0,0,0)]],
              "deployment_code": 1,
              "chromosome_bases": ['A', 'T', 'G', 'C'],
              "background_mutation": 0.1,
              "additional_mutation": 0,
              "mutation_type": 'point',
              "chromosome_size": 300,
              "genome_size": 1,
              "max_tape_length": 50,
              "clean_cell": False,
              "interpreter": 'ragaraja',
              "interpret_chromosome": True,
              "max_codon": 2000,
              "population_size": 1,
              "eco_cell_capacity": 100,
              "world_x": 5,
              "world_y": 5,
              "world_z": 5,
              "goal": 0,
              "maximum_generations": 100,
              "fossilized_ratio": 0.01,
              "fossilized_frequency": 20,
              "print_frequency": 10,
              "ragaraja_version": 0.2,
              "ragaraja_instructions": [],
              "eco_buried_frequency": 100,
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
