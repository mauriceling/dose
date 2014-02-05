'''
Example 09c: Extending from Example 09a (as baseline) and Example 09b 
(short distance migration) to examine the effects of long distance 
migration (across one or more eco-cells)  on genetic distance differences 
from an initially identical population (development of sub-populations or 
demes which may lead to speciation)

This example is identical to Example 05, except background mutation rate is 
changed from 10% in Example 03 to 0.1% in this example.

In this simulation,
    - 1 populations of 1250 organisms
    - each organism will have 1 chromosome of only 2 bases (1 and 0)
    - Evenly deployed across 25 eco-cells (50 organism per eco-cell)
    - 20% background point mutation on chromosome of 50 bases
    - 10% organism movement per eco-cell per generation throughout the 
    simulation
    - the same organism may move twice due to sequential evaluation of the 
    eco-cells but the probability of such event will be 10% x 10% = 1%; 
    similarly, 3 or more movement by the same organism may happen with 
    reducing probabilities
    - the destination eco-cell for movement is random; thus, from 25 
    possible eco-cells, there is a probability of 4% chance of relocating 
    back to the same (original) eco-cell, 16% chance of relocating to one 
    of the 4-neighbour eco-cells and 32% chance of relocating to one of the 
    8-neighbour eco-cells
    - no Ragaraja interpretation of genome
    - 1000 generations to be simulated
'''
# needed to run this example without prior
# installation of DOSE into Python site-packages
import run_examples_without_installation

# Example codes starts from here
import dose, genetic, random
import simulation_calls as helper

parameters = {
              "simulation_name": "09_long_migration_isolated_mating",
              "population_names": ['pop_01'],
              "population_locations": [[(x,y,z) 
                                        for x in xrange(5) 
                                            for y in xrange(5) 
                                                for z in xrange(1)]],
              "deployment_code": 3,
              "chromosome_bases": ['0','1'],
              "background_mutation": 0.001,
              "additional_mutation": 0,
              "mutation_type": 'point',
              "chromosome_size": 5000,
              "genome_size": 1,
              "max_tape_length": 50,
              "clean_cell": True,
              "interpret_chromosome": False,
              "max_codon": 2000,
              "population_size": 1250,
              "eco_cell_capacity": 50,
              "world_x": 5,
              "world_y": 5,
              "world_z": 1,
              "goal": 0,
              "maximum_generations": 1000,
              "fossilized_ratio": 0.01,
              "fossilized_frequency": 100,
              "print_frequency": 10,
              "ragaraja_version": 0,
              "ragaraja_instructions": ['000', '001', '010', 
                                        '011', '100', '101'],
              "eco_buried_frequency": 1250,
              "database_file": "sim09_long_migration.db",
              "database_logging_frequency": 1
             }

class simulation_functions(dose.dose_functions):

    def organism_movement(self, Populations, pop_name, World): pass

    def organism_location(self, Populations, pop_name, World): 
        for location in parameters["population_locations"][0]:
            group = dose.filter_location(location, Populations[pop_name].agents)
            for i in xrange(int(round((len(group) * 0.1)))):
                (x,y,z) = helper.coordinates(location)
                World.ecosystem[x][y][z]['organisms'] -= 1
                immigrant = random.choice(Populations[pop_name].agents)
                while immigrant not in group:
                    immigrant = random.choice(Populations[pop_name].agents)
                new_location = random.choice(parameters["population_locations"][0])
                while new_location == location:
                    new_location = random.choice(parameters["population_locations"][0])
                immigrant.status['location'] = new_location
                (x,y,z) = helper.coordinates(new_location)
                World.ecosystem[x][y][z]['organisms'] += 1

    def ecoregulate(self, World): pass

    def update_ecology(self, World, x, y, z): pass

    def update_local(self, World, x, y, z): pass

    def report(self, World): pass

    def fitness(self, Populations, pop_name): pass

    def mutation_scheme(self, organism): 
        organism.genome[0].rmutate(parameters["mutation_type"],
                                   parameters["additional_mutation"])

    def prepopulation_control(self, Populations, pop_name): pass

    def mating(self, Populations, pop_name): 
        for location in parameters["population_locations"][0]:
            group = dose.filter_location(location, Populations[pop_name].agents)
            for x in xrange(len(group)/2):
                parents = []
                for i in xrange(2):
                    parents.append(random.choice(Populations[pop_name].agents))
                    while parents[i] not in group:
                        parents[i] = random.choice(Populations[pop_name].agents)
                    Populations[pop_name].agents.remove(parents[i])
                crossover_pt = random.randint(0, len(parents[0].genome[0].sequence))
                (new_chromo1, new_chromo2) = genetic.crossover(parents[0].genome[0], 
                                                               parents[1].genome[0], 
                                                               crossover_pt)
                children = [genetic.Organism([new_chromo1],
                                             parameters["mutation_type"],
                                             parameters["additional_mutation"]),
                            genetic.Organism([new_chromo2],
                                             parameters["mutation_type"],
                                             parameters["additional_mutation"])]
                for child in children:
                    child.status['parents'] = [parents[0].status['identity'], 
                                               parents[1].status['identity']]
                    child.status['location'] = location
                    child.generate_name()
                    child.status['deme'] = pop_name
                    Populations[pop_name].agents.append(child)

    def postpopulation_control(self, Populations, pop_name): pass

    def generation_events(self, Populations, pop_name): pass

    def population_report(self, Populations, pop_name):
        report_list = []
        for organism in Populations[pop_name].agents:
            identity = str(organism.status['identity'])
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
