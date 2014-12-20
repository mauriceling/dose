'''
Example 11: Examining the effects of natural selection on a 
population's genetic pool by implementing a fitness scheme 
along with a goal to be reached from a randomly deployed population. 

In this simulation,
    - 1 population of 750 organisms
    - each organism will have 1 chromosome of only 2 bases (1 and 0)
    - Evenly deployed across 25 eco-cells (30 organism per eco-cell)
    - 1% background point mutation on chromosome of 50 bases
    - 2% additional mutation
    - no organism movement throughout the simulation
    - no Ragaraja interpretation of genome
    - 1000 generations to be simulated
    - Fitness score goal of 700
'''
# needed to run this example without prior
# installation of DOSE into Python site-packages
try: 
	import run_examples_without_installation
except ImportError: pass

# Example codes starts from here
import dose, random
from collections import Counter

parameters = {
              "simulation_name": "example_11",
              "population_names": ['pop_01'],
              "population_locations": [[(x,y,z) for x in range(5) for y in range(5) for z in range(1)]],
              "deployment_code": 3,
              "chromosome_bases": ['0','1'],
              "background_mutation": 0.00,
              "additional_mutation": 0.01,
              "mutation_type": 'point',
              "chromosome_size": 1000,
              "genome_size": 1,
              "max_tape_length": 50,
              "clean_cell": True,
              "interpret_chromosome": False,
              "max_codon": 2000,
              "population_size": 750,
              "eco_cell_capacity": 30,
              "world_x": 5,
              "world_y": 5,
              "world_z": 1,
              "goal": 700,
              "maximum_generations": 100,
              "fossilized_ratio": 0.01,
              "fossilized_frequency": 100,
              "print_frequency": 1,
              "ragaraja_version": 0,
              "ragaraja_instructions": ['000', '001', '010', 
                                        '011', '100', '101'],
              "eco_buried_frequency": 100,
              "database_file": "sim11_no_migration.db",
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
            fitness_score = 0
            for base in organism.genome[0].sequence:
                if int(base) != 0: fitness_score = fitness_score + 1
            organism.status['fitness'] = fitness_score

    def mutation_scheme(self, organism): 
        if organism.status['fitness'] != parameters["goal"]:
            organism.genome[0].rmutate(parameters["mutation_type"],
                                       parameters["additional_mutation"])

    def prepopulation_control(self, Populations, pop_name):
        for location in parameters["population_locations"][0]:
            group = dose.filter_location(location, Populations[pop_name].agents)
            average_fitness = sum([organism.status["fitness"] for organism in group])/len(group)
            if average_fitness != parameters["goal"]:
                alpha_organism_fitness = 0
                for organism in group:
                    if abs(parameters["goal"] - organism.status['fitness']) < \
                        abs(parameters["goal"] - alpha_organism_fitness):
                        alpha_organism_fitness = int(organism.status['fitness'])
                for organism in group:
                    if organism.status['fitness'] not in range(alpha_organism_fitness - 2,
                                                                alpha_organism_fitness + 2):
                        Populations[pop_name].agents.remove(organism)
            else:
                if organism.status['fitness'] != parameters["goal"]:
                    Populations[pop_name].agents.remove(organism)

    def mating(self, Populations, pop_name): 
        for location in parameters["population_locations"][0]:
            group = dose.filter_location(location, Populations[pop_name].agents)
            for x in range(parameters["eco_cell_capacity"] - len(group)):
                parents = []
                alpha_organism = group[0]
                for organism in group:
                    if abs(parameters["goal"] - organism.status['fitness']) < \
                        abs(parameters["goal"] - alpha_organism.status['fitness']):
                        alpha_organism = organism
                parents.append(alpha_organism)
                parents.append(random.choice(group))
                crossover_pt = random.randint(0, len(parents[0].genome[0].sequence))
                (new_chromo1, new_chromo2) = dose.genetic.crossover(parents[0].genome[0], 
                                                               parents[1].genome[0], 
                                                               crossover_pt)
                child = dose.genetic.Organism([new_chromo1],
                                         parameters["mutation_type"],
                                         parameters["additional_mutation"])
                child.status['parents'] = [parents[0].status['identity'],
                                           parents[1].status['identity']]
                child.status['location'] = location
                child.generate_name()
                child.status['deme'] = pop_name
                Populations[pop_name].agents.append(child)

    def postpopulation_control(self, Populations, pop_name):
        for location in parameters["population_locations"][0]:
            group = dose.filter_location(location, Populations[pop_name].agents)
            average_fitness = sum([organism.status["fitness"] for organism in group])/len(group)
            if average_fitness != parameters["goal"]:
                omega_organism_fitness = 0
                for organism in group:
                    if abs(parameters["goal"] - organism.status['fitness']) > \
                        abs(parameters["goal"] - omega_organism_fitness):
                        omega_organism_fitness = int(organism.status['fitness'])
                for organism in group:
                    if organism.status['fitness'] in range(omega_organism_fitness - 2,
                                                            omega_organism_fitness + 2):
                        Populations[pop_name].agents.remove(organism)
            else:
                if organism.status['fitness'] != parameters["goal"]:
                    Populations[pop_name].agents.remove(organism)

    def generation_events(self, Populations, pop_name): pass

    def population_report(self, Populations, pop_name):
        report_list = []
        for organism in Populations[pop_name].agents:
            identity = str(organism.status['fitness'])
            report_list.append(identity)
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