# needed to run this example without prior
# installation of DOSE into Python site-packages
import run_examples_without_installation

# Example codes starts from here
import dose, genetic, random

parameters = {
              "simulation_name": "03_no_migration_isolated_mating",
              "population_names": ['pop_01'],
              "population_locations": [[(x,y,z) for x in xrange(5) for y in xrange(5) for z in xrange(1)]],
              "deployment_code": 3,
              "chromosome_bases": ['0','1'],
              "background_mutation": 0.1,
              "additional_mutation": 0,
              "mutation_type": 'point',
              "chromosome_size": 50,
              "genome_size": 1,
              "cells": 50,
              "max_cell_population": 200,
              "clean_cell": True,
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
              "ragaraja_version": 2,
              "eco_buried_frequency": 1000,
             }

class simulation_functions():

    def organism_movement(self, World, x, y, z): pass

    def organism_location(self, World, x, y, z): pass

    def ecoregulate(self, World): pass

    def update_ecology(self, World, x, y, z): pass

    def update_local(self, World, x, y, z): pass

    def report(World): pass

    def fitness(self, Populations, pop_name): pass

    def mutation_scheme(self, organism): 
        organism.genome[0].rmutate(parameters["mutation_type"],
                                   parameters["additional_mutation"])

    def prepopulation_control(self, Populations, pop_name): pass

    def mating(self, Populations, pop_name):
        for location in parameters["population_locations"][0]:
            group = dose.filter_location(location, Populations[pop_name].agents)
            temp = []
            for x in xrange(len(group)):
                organism1 = group[random.randint(0, len(group) - 1)]
                organism2 = group[random.randint(0, len(group) - 1)]
                crossover_pt = random.randint(0, len(organism1.genome[0].sequence))
                (g1, g2) = genetic.crossover(organism1.genome[0], organism2.genome[0], crossover_pt)
            new_org = genetic.Organism([g1])
            new_org.status['location'] = location
            new_org.generate_name()
            new_org.status['deme'] = pop_name
            temp = temp + [new_org]
        Populations[pop_name].agents + temp

    def postpopulation_control(self, Populations, pop_name): pass

    def generation_events(self, Populations, pop_name): pass

    def population_report(self, Populations, pop_name):
        sequences = [''.join(org.genome[0].sequence) for org in Populations[pop_name].agents]
        identities = [org.status['identity'] for org in Populations[pop_name].agents]
        locations = [str(org.status['location']) for org in Populations[pop_name].agents]
        demes = [org.status['deme'] for org in Populations[pop_name].agents]
        return '\n'.join(locations)

    def deployment_scheme(Populations, pop_name, World): pass

dose.simulate(parameters, simulation_functions)
