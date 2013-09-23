import sys, os, random
from datetime import datetime

import ragaraja
import register_machine
import dose_world
import genetic

p = {
     "simulation_code": "SIM_01",
     "starting_time": datetime.utcnow(),
     "population_names": ['pop_01','pop_02'],
     "population_locations": [(0,0,0), (4,4,4)],
     "chromosome_bases": ['0','1'],
     "background_mutation": 0.2,
     "additional_mutation": 0,
     "mutation_type": 'point',
     "chromosome_size": 30,
     "genome_size": 1,
     "cells": 50,
     "max_cell_population": 200,
     "clean_cell": True,
     "max_codon": 2000,
     "population_size": 50,
     "eco_cell_capacity": 50,
     "world_x": 5,
     "world_y": 5,
     "world_z": 5,
     "goal": 0,
     "maximum_generations": 500,
     "fossilized_ratio": 0.01,
     "fossilized_frequency": 100,
     "print_frequency": 10,
     "ragaraja_version": 2,
     "eco_buried_frequency": 500,
    }

class custom_functions():
    cell = [0] * p["cells"]
    def fitness(self): pass
    def mutation_scheme(self, organism): 
        organism.genome[0].rmutate(p["mutation_type"],p["additional_mutation"])
    def get_cell(self):
        return ','.join([str(x) for x in self.cell])
    def prepopulation_control(self): pass
    def mating(self): pass
    def postpopulation_control(self): pass
    def generation_events(self): pass
    def population_report(self, population):
        sequences = [''.join(org.genome[0].sequence) for org in population.agents]
        return '\n'.join(sequences)


overwrite = custom_functions()

class world(dose_world.World):
    def __init__(self, world_x = p["world_x"],
                 world_y = p["world_y"],
                 world_z = p["world_z"]):
        super(world, self).__init__(world_x, world_y, world_z)
    def organism_movement(self, x, y, z): pass
    def organism_location(self, x, y, z): pass
    def ecoregulate(self): pass
    def update_ecology(self, x, y, z): pass
    def update_local(self, x, y, z): pass
    def report(self): pass

p.update({"initial_chromosome":['0'] * p["chromosome_size"],
          "mutation_scheme": overwrite.mutation_scheme,
          "fitness_function": overwrite.fitness,
          "prepopulation_control": overwrite.prepopulation_control,
          "mating": overwrite.mating,
          "postpopulation_control": overwrite.postpopulation_control,
          "generation_events": overwrite.generation_events,
          "population_report": overwrite.population_report})

def spawn_populations(populations):
    temp_pop = {}
    for population in p["population_names"]:
        temp_pop[population] = genetic.population_constructor(p)
    return temp_pop


def eco_cell_locator(function):
    for x in range(p["world_x"]):
        for y in range(p["world_y"]):
            for z in range(p["world_z"]):
                function(x,y,z)

def eco_cell_executor(function):
    for x in range(p["world_x"]):
        for y in range(p["world_y"]):
            for z in range(p["world_z"]):
                function()

def coordinates(location):
    x = location[0]
    y = location[1]
    z = location[2]
    return (x,y,z)

def deploy(population):
    location = p["population_locations"][p["population_names"].index(population)]
    (x,y,z) = coordinates(location)
    World.ecosystem[x][y][z]['organisms'] = p["population_size"]
    for individual in Populations[population].agents:
        individual.status['location'] = location

def interpret_chromosome(population):
    for individual in Populations[population].agents:
        location = individual.status['location']
        (x,y,z) = coordinates(location)
        inputdata = World.ecosystem[x][y][z]['local_input']
        output = World.ecosystem[x][y][z]['local_output']
        source = ''.join(individual.genome[0].sequence)

        if p["clean_cell"]:
            array = [0] * p["cells"]
        else:
            array = individual.overwrite.cell
        
        try: (array, apointer, inputdata, output, source, spointer) = \
            register_machine.interpret(source, ragaraja.ragaraja, 3,
                                       inputdata, array,
                                       p["max_cell_population"], p["max_codon"])
        except Exception: pass
            
        individual.cell = array
        World.ecosystem[x][y][z]['temporary_input'] = inputdata
        World.ecosystem[x][y][z]['temporary_output'] = output

def step(population):
    if Populations[population].generation > 0:
        overwrite.prepopulation_control()
    overwrite.mating()
    overwrite.postpopulation_control()
    for organism in Populations[population].agents:
        overwrite.mutation_scheme(organism)
    overwrite.generation_events()
    Populations[population].generation += 1
    return overwrite.population_report(Populations[population])

def report_generation(population):
    report = step(population)
    if generation_count % int(p["fossilized_frequency"]) == 0:
        file = '%s_%s_' % (p["simulation_code"], population)
        Populations[population].freeze(file, p["fossilized_ratio"])
    if generation_count % int(p["print_frequency"]) == 0:
        print '\nGENERATION: %s \n%s' % (str(generation_count), str(report))
        f = open(('%s_%s.result.txt' % (p["simulation_code"], population)), 'a')
        dtstamp = str(datetime.utcnow())
        f.write('\n'.join(['\n' + dtstamp, 'GENERATION: ' + str(generation_count), str(report)]))
        f.write('\n')
        f.close

def bury_world(generation_count):
    if generation_count % int (p["eco_buried_frequency"]) == 0:
       filename = '%s_gen%s.eco' % (p["simulation_code"], str(generation_count))
       World.eco_burial(filename)

Populations = spawn_populations(p["population_names"])
World = world()

def write_parameters():
    for population in Populations:
        f = open(('%s_%s.result.txt' % (p["simulation_code"], population)), 'a')
        f.write('''SIMULATION CODE: %(simulation_code)s                     %(starting_time)s
----------------------------------------------------------------------

population_names: %(population_names)s
population_locations: %(population_locations)s
chromosome_bases: %(chromosome_bases)s
initial_chromosome: %(initial_chromosome)s
background_mutation: %(background_mutation)s
additional_mutation: %(additional_mutation)s
mutation_type: %(mutation_type)s
chromosome_size: %(chromosome_size)s
genome_size: %(genome_size)s
cells: %(cells)s
max_cell_population: %(max_cell_population)s
clean_cell: %(clean_cell)s
max_codon: %(max_codon)s
population_size: %(population_size)s
eco_cell_capacity: %(eco_cell_capacity)s
world_x: %(world_x)s
world_y: %(world_y)s
world_z: %(world_z)s
goal: &(goal)s
maximum_generations: %(maximum_generations)s
fossilized_ratio: %(fossilized_ratio)s
fossilized_frequency: %(fossilized_frequency)s
print_frequency: %(print_frequency)s
ragaraja_version: %(ragaraja_version)s
eco_buried_frequency: %(eco_buried_frequency)s

REPORT:
----------------------------------------------------------------------
''' % p)
        f.close()

if __name__ == "__main__":

    ragaraja.activate_version(p["ragaraja_version"])

    write_parameters()

    for population in Populations:
        deploy(population)
    
        generation_count = 0
        while generation_count < p["maximum_generations"]:
            generation_count += 1
            World.ecoregulate()
            
            eco_cell_locator(World.update_ecology)
            eco_cell_locator(World.update_local)

            interpret_chromosome(population)

            report_generation(population)

            eco_cell_locator(World.organism_movement)
            eco_cell_locator(World.organism_location)

            eco_cell_executor(World.report)

            bury_world(generation_count)
