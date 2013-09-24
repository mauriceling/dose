import dose

parameters = {
              "simulation_code": "SIM_01",
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

class entities(dose.dose_entities):

    def __init__(self, world_x = parameters["world_x"],
                 world_y = parameters["world_y"],
                 world_z = parameters["world_z"]):
        super(entities, self).__init__(world_x, world_y, world_z)
        
    def organism_movement(self, x, y, z): pass
    def organism_location(self, x, y, z): pass
    def ecoregulate(self): pass
    def update_ecology(self, x, y, z): pass
    def update_local(self, x, y, z): pass
    def report(self): pass
    
    cell = [0] * parameters["cells"]
    def fitness(self): pass
    def mutation_scheme(self, organism): 
        organism.genome[0].rmutate(parameters["mutation_type"],
                                   parameters["additional_mutation"])
    def prepopulation_control(self): pass
    def mating(self): pass
    def postpopulation_control(self): pass
    def generation_events(self): pass
    def population_report(self, population):
        sequences = [''.join(org.genome[0].sequence) for org in population.agents]
        return '\n'.join(sequences)

dose.simulate(parameters, entities)
