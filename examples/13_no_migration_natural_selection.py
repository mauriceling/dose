'''
Example 13: Examining the effects of natural selection on a 
population's genetic pool by implementing a fitness scheme that counts
a specific sequence within the chromosome along with a goal to be reached 
from an evenly deployed population.

In this simulation,
    - 1 population of 500 organisms
    - each organism will have 1 chromosome of only 2 bases (1 and 0)
    - Evenly deployed across 5 eco-cells (100 organism per eco-cell)
    - 10% background point mutation on chromosome of 50 bases
    - no organism movement throughout the simulation
    - no Ragaraja interpretation of genome
    - 200 generations to be simulated
    - Fitness score goal of 55
'''
# needed to run this example without prior
# installation of DOSE into Python site-packages
import run_examples_without_installation

# Example codes starts from here
import dose, genetic, random
from collections import Counter

parameters = {
              "simulation_name": "example_13",
              "population_names": ['pop_01'],
              "population_locations": [[(x,0,0) for x in xrange(5)]],
              "initial_chromosome": ['1','0'] * 50,
              "deployment_code": 3,
              "chromosome_bases": ['0','1'],
              "background_mutation": 0.1,
              "additional_mutation": 0.00,
              "mutation_type": 'point',
              "chromosome_size": 100,
              "genome_size": 1,
              "max_tape_length": 50,
              "clean_cell": True,
              "interpret_chromosome": False,
              "max_codon": 2000,
              "population_size": 500,
              "eco_cell_capacity": 100,
              "world_x": 5,
              "world_y": 1,
              "world_z": 1,
              "goal": 55,
              "maximum_generations": 200,
              "fossilized_ratio": 0.01,
              "fossilized_frequency": 50,
              "print_frequency": 1,
              "ragaraja_version": 0,
              "ragaraja_instructions": ['000', '001', '010', 
                                        '011', '100', '101'],
              "eco_buried_frequency": 200,
              "database_file": "sim13_no_migration.db",
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
            chromosome = organism.genome[0].sequence
            zero_count = []
            for base_index in xrange(parameters["chromosome_size"] - 1):
                if int(chromosome[base_index]) == 0 and int(chromosome[base_index - 1]) != 0:
                    next_index = 1
                    while int(chromosome[next_index + base_index]) == 0:
                        next_index += 1
                        if (next_index + base_index) == parameters["chromosome_size"]: break
                    zero_count.append(next_index - 1)
            organism.status['fitness'] = max(zero_count)

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
                    if organism.status['fitness'] not in xrange(alpha_organism_fitness - 2,
                                                                alpha_organism_fitness + 2):
                        Populations[pop_name].agents.remove(organism)
            else:
                if organism.status['fitness'] != parameters["goal"]:
                    Populations[pop_name].agents.remove(organism)

    def mating(self, Populations, pop_name): 
        for location in parameters["population_locations"][0]:
            group = dose.filter_location(location, Populations[pop_name].agents)
            for x in xrange(parameters["eco_cell_capacity"] - len(group)):
                parents = []
                alpha_organism = group[0]
                for organism in group:
                    if abs(parameters["goal"] - organism.status['fitness']) < \
                        abs(parameters["goal"] - alpha_organism.status['fitness']):
                        alpha_organism = organism
                parents.append(alpha_organism)
                parents.append(random.choice(group))
                crossover_pt = random.randint(0, len(parents[0].genome[0].sequence))
                (new_chromo1, new_chromo2) = genetic.crossover(parents[0].genome[0], 
                                                               parents[1].genome[0], 
                                                               crossover_pt)
                child = genetic.Organism([new_chromo1],
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
                    if organism.status['fitness'] in xrange(omega_organism_fitness - 1,
                                                            omega_organism_fitness + 1):
                        Populations[pop_name].agents.remove(organism)
            else:
                if organism.status['fitness'] != parameters["goal"]:
                    Populations[pop_name].agents.remove(organism)

    def generation_events(self, Populations, pop_name): pass

    def population_report(self, Populations, pop_name):
        report_list = []
        for organism in Populations[pop_name].agents:
            chromosome = ''.join(organism.genome[0].sequence)
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