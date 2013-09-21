import sys, os
from datetime import datetime

import ragaraja as N
import genetic as g
import dose_world as w
import register_machine as r

parameters = {
              "simulation_code":"SIM_O1",
              "starting_time": datetime.utcnow(),
              "population_names":['pop_01','pop_02'],
              "population_locations":[(0,0,0), (4,4,4)],
              "chromosome_bases":['0','1'],
              "background_mutation_rate":0.01,
              "additional_mutation_rate":0,
              "chromosome_size":30,
              "cells":50,
              "max_cell_population":200,
              "clean_cell":True,
              "max_codon":2000,
              "population_size":20,
              "maximum_cell_capacity":50,
              "world_x":5,
              "world_y":5,
              "world_z":5,
              "maximum_generations":500,
              "fossilized_ratio":0.01,
              "fossilized_frequency":250,
              "print_frequency":10,
              "ragaraja_version":2,
              "eco_buried_frequency":500,
              }

Chromosome = g.Chromosome((['0'] * parameters["chromosome_size"]),parameters["chromosome_bases"],parameters["background_mutation_rate"])

class Organism(g.Organism):

    cell = [0] * parameters["cells"]

    def __init__(self): 
        self.genome = [Chromosome.replicate()]
    def get_cell(self):
        return ','.join([str(x) for x in self.cell])
    def mutation_scheme(self):
        self.genome[0].rmutate('point', 0)

class Population(g.Population):
    def __init__(self):
        self.agents = [Organism() for x in xrange(parameters["population_size"])]
        self.maxgenerations = parameters["maximum_generations"]
        self.generation = 0
    def report(self):
        sequences = [''.join(org.genome[0].sequence) for org in self.agents]
        return '\n'.join(sequences)
    
class World(w.World):
    def __init__(self):
        super(World, self).__init__(world_x=parameters["world_x"], world_y=parameters["world_y"], world_z=parameters["world_z"])
        
def simulate():
    populations = {}
    world = World()

    for i in range(len(parameters["population_names"])):
        population_name = parameters["population_names"][i]
        population_location = parameters["population_locations"][i]
        world_x = population_location[0]
        world_y = population_location[1]
        world_z = population_location[2]
        deme = Population()
        for individual in deme.agents:
            individual.status['location'] = population_location
        world.ecosystem[world_x][world_y][world_z]['organisms'] = \
            len(deme.agents)
        populations[population_name] = deme

    generation_count = 0
    while generation_count < parameters["maximum_generations"]:
        generation_count += 1

        world.ecoregulate()

        for x in range(world.world_x):
            for y in range(world.world_y):
                for z in range(world.world_z):
                    world.update_ecology(x, y, z)
                    world.update_local(x, y, z)
        
        for name in parameters["population_names"]:
            for i in range(len(populations[name].agents)):
                source = populations[name].agents[i].genome[0].sequence
                source = ''.join(source)
                if parameters["clean_cell"]:
                    array = [0] * parameters["cells"]
                else:
                    array = populations[name].agents[i].cell
                location = populations[name].agents[i].status['location']
                world_x = location[0]
                world_y = location[1]
                world_z = location[2]
                inputdata = world.ecosystem[world_x][world_y][world_z]['local_input']
                try: (array, apointer, inputdata, output, source, spointer) = \
                    r.interpret(source, N.ragaraja, 3, inputdata, array, parameters["maximum_cell_capacity"], parameters["max_codon"])
                except IndexError: pass
                except ZeroDivisionError: pass
                except OverflowError: pass
                except ValueError: pass
                populations[name].agents[i].cell = array
                world.ecosystem[world_x][world_y][world_z]['temporary_input'] = inputdata
                world.ecosystem[world_x][world_y][world_z]['temporary_output'] = output
            
            report = populations[name].generation_step()
            if generation_count % int(parameters["fossilized_frequency"]) == 0:
                file = name + '_'
                populations[name].freeze(file, parameteres["fossilized_ratio"])
            if generation_count % int(parameters["print_frequency"]) == 0:
                print str(generation_count), str(report)
                f = open(name + '.result.txt', 'a')
                dtstamp = str(datetime.utcnow())
                f.write('-'.join([dtstamp, str(generation_count), str(report)]))
                f.write('\n')
                f.close

        for x in range(world.world_x):
            for y in range(world.world_y):
                for z in range(world.world_z):
                    world.organism_movement(x, y, z)
                    world.organism_location(x, y, z)
                    world.report()

        if generation_count % int(parameters["eco_buried_frequency"]) == 0:
            filename = 'eco_' + str(generation_count) + '.eco'
            world.eco_burial(filename)

def set_instruction_version():
    if parameters["ragaraja_version"] == 0:
        f = open('ragaraja_instructions.txt', 'r').readlines()
        f = [x[:-1].split('=') for x in f]
        f = [x[0] for x in f if x[1] == 'Y']
        ragaraja_instructions = f
    if parameters["ragaraja_version"] == 0.1:
        ragaraja_instructions = N.nBF_instructions
    if parameters["ragaraja_version"] == 1:
        ragaraja_instructions = N.ragaraja_v1
    if parameters["ragaraja_version"] == 2:
        ragaraja_instructions = N.ragaraja_v2
    for instruction in N.ragaraja:
        if instruction not in ragaraja_instructions:
            N.ragaraja[instruction] = N.not_used
    return ragaraja_instructions

def write_parameters():
    for name in parameters["population_names"]:
        f = open(name + '.result.txt', 'a')
        f.write('''SIMULATION CODE: %(simulation_code)s                 %(starting_time)s
----------------------------------------------------------------------
population_names: %(population_names)s
population_locations: %(population_locations)s
chromosome_bases: %(chromosome_bases)s
background_mutation_rate: %(background_mutation_rate)s
additional_mutation_rate: %(additional_mutation_rate)s
chromosome_size: %(chromosome_size)s
cells: %(cells)s
max_cell_population: %(max_cell_population)s
clean_cell: %(clean_cell)s
max_codon: %(max_codon)s
population_size: %(population_size)s
maximum_cell_capacity: %(maximum_cell_capacity)s
world_x: %(world_x)s
world_y: %(world_y)s
world_z: %(world_z)s
maximum_generations: %(maximum_generations)s
fossilized_ratio: %(fossilized_ratio)s
fossilized_frequency: %(fossilized_frequency)s
print_frequency: %(print_frequency)s
ragaraja_version: %(ragaraja_version)s
eco_buried_frequency: %(eco_buried_frequency)s
----------------------------------------------------------------------
REPORT:

        ''' % parameters)
        f.close()

if __name__ == "__main__":
    ragaraja_instructions = set_instruction_version()
    write_parameters()
    simulate()
