'''
Example 32: Construct World and 2 Populations from scratch (Example 31 
is constructing 1 population from scratch).

In this simulation,
    - construct world
    - construct 1 population of 5 organisms with different genome 
    for each organism
    - 100 generations to be simulated
'''
# needed to run this example without prior
# installation of DOSE into Python site-packages
try: 
	import run_examples_without_installation
except ImportError: pass

# Example codes starts from here
from pprint import pprint
import random
import dose


parameters = {# Part 1: Simulation metadata
              "simulation_name": "32_construct_simulation",
              "population_names": ['pop_01', 'pop_02'],

              # Part 2: World settings
              "world_x": 1,
              "world_y": 1,
              "world_z": 1,
              "population_locations": None,
              "eco_cell_capacity": 100,
              "deployment_code": None,

              # Part 3: Population settings
              "population_size": 10,

              # Part 4: Genetics settings
              "genome_size": 1,
              "chromosome_size": 100,
              "chromosome_bases": ['A', 'T', 'G', 'C'],
              "initial_chromosome": ['A', 'T', 'G', 'C'] * 25,

              # Part 5: Mutation settings
              "background_mutation": 0.05,
              "additional_mutation": 0,
              "mutation_type": 'point',
              
              # Part 6: Metabolic settings
              "interpreter": None,
              "instruction_size": None,
              "ragaraja_version": None,
              "base_converter": None,
              "ragaraja_instructions": [],
              "max_tape_length": None,
              "interpret_chromosome": False,
              "clean_cell": None,
              "max_codon": None,

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
        for org in Populations[pop_name].agents:
          generation = str(org.status["generation"])
          deme = org.status['deme']
          identity = str(org.status['identity'])
          sequence = str(''.join(org.genome[0].sequence))
          print("|".join([generation, deme, identity, sequence]))

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

# Step 1: Construct World
print('Constructing World entity...')
# World(parameters["world_x"], parameters["world_y"], parameters["world_z"])
World = dose.dose_world.World(1, 1, 1)
World = dose.load_all_local_input(World, [1, 2])

# Step 2: Construct Population(s)
pop_01 = {}
for i in range(1, 6):
  identity = "O" + str(i)
  genome = [[random.choice(["A", "T", "G", "C"]) for i in range(100)]]
  pop_01[identity] = {"status": {"alive": True, "vitality": 100.0, 
                                 "parents": None, "age": 0.0, 
                                 "gender": None, "lifespan": 100.0, 
                                 "fitness": 0.0, "blood": None, 
                                 "identity": identity, "deme": "pop_01", 
                                 "location": (0,0,0), "generation": 0, 
                                 "death": None},
                     "genome": genome,
                     "bases": parameters["chromosome_bases"],
                     "background_mutation": parameters["background_mutation"],
                     "additional_mutation": parameters["additional_mutation"],
                     "mutation_type": parameters["mutation_type"]}
pop_02 = {}
for i in range(1, 6):
  identity = "T" + str(i)
  genome = [[random.choice(["A", "T", "G", "C"]) for i in range(100)]]
  pop_02[identity] = {"status": {"alive": True, "vitality": 100.0, 
                                 "parents": None, "age": 0.0, 
                                 "gender": None, "lifespan": 100.0, 
                                 "fitness": 0.0, "blood": None, 
                                 "identity": identity, "deme": "pop_02", 
                                 "location": (0,0,0), "generation": 0, 
                                 "death": None},
                     "genome": genome,
                     "bases": parameters["chromosome_bases"],
                     "background_mutation": parameters["background_mutation"],
                     "additional_mutation": parameters["additional_mutation"],
                     "mutation_type": parameters["mutation_type"]}

def construct_PopDiffOrg(World, parameters, population_dictionary):
  organisms = []
  for org_key in population_dictionary:
    orgData = population_dictionary[org_key]
    chromosomes = [dose.genetic.Chromosome(chr_seq,
                    orgData["bases"], orgData["background_mutation"])
                    for chr_seq in orgData["genome"]]
    organism = dose.genetic.Organism(chromosomes,
                                      orgData['mutation_type'],
                                      orgData['additional_mutation'])
    organism.status = orgData["status"]
    x = orgData["status"]["location"][0]
    y = orgData["status"]["location"][1]
    z = orgData["status"]["location"][2]
    World.ecosystem[x][y][z]["organisms"] = World.ecosystem[x][y][z]["organisms"] + 1
    organisms.append(organism)
  population = dose.genetic.Population(parameters["goal"],
                                       parameters["maximum_generations"],
                                       organisms)
  return (World, population)

(World, population_01) = construct_PopDiffOrg(World, parameters, pop_01)
(World, population_02) = construct_PopDiffOrg(World, parameters, pop_02)
Populations = {'pop_01': population_01, 'pop_02': population_02}

# Step 3: Simulate
print('\nStarting simulation on sequential ecological cell simulator...')
(simulation_functions, parameters, Populations, World) = \
    dose.sequential_simulator(simulation_functions, parameters, 
                              Populations, World)
print('\nSimulation ended...')

# =================== Print out to check =============================
print("Population Dictionary")
for k in pop_01:
  print("Key: " + k)
  print(pop_01[k])
for k in pop_02:
  print("Key: " + k)
  print(pop_02[k])
print("")
print("World: " + str(World))
print("World.ecosystem:")
pprint(World.ecosystem)
print("")
print("Populations: " + str(Populations))
print("")
print("Organisms in pop_01 (Populations['pop_01'].agents):")
pprint(Populations['pop_01'].agents)
print("")
print("Organisms in pop_02 (Populations['pop_02'].agents):")
pprint(Populations['pop_02'].agents)
print("")
print("Genome of Organism 1 in pop_01 (Populations['pop_01'].agents[0].genome):")
pprint(Populations['pop_01'].agents[0].genome)
print("")
print("Sequence of Chromosome 1 of Organism 1 in pop_01 (Populations['pop_01'].agents[0].genome[0].sequence):") 
print(Populations['pop_01'].agents[0].genome[0].sequence)
print("")
print("Bases of Chromosome 1 of Organism 1 in pop_01 (Populations['pop_01'].agents[0].genome[0].base):")
print(Populations['pop_01'].agents[0].genome[0].base)
print("")
print("Background mutation rate of Chromosome 1 of Organism 1 in pop_01 (Populations['pop_01'].agents[0].genome[0].background_mutation): " + str(Populations['pop_01'].agents[0].genome[0].background_mutation))
# =================== Print out to check =============================
