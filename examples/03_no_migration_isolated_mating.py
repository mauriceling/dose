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
              "background_mutation": 0.2,
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

class simulation_functions(dose.dose_functions):

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
                    child.status['location'] = location
                    child.generate_name()
                    child.status['deme'] = pop_name
                    Populations[pop_name].agents.append(child)

    def postpopulation_control(self, Populations, pop_name): pass

    def generation_events(self, Populations, pop_name): pass

    def population_report(self, Populations, pop_name):
        report_list = []
        for organism in Populations[pop_name].agents:
            chromosome = ''.join(organism.genome[0].sequence)
            location = str(organism.status['location'])
            report_list.append(chromosome + '  ' + location)
        return '\n'.join(report_list)

    def deployment_scheme(Populations, pop_name, World): pass

dose.simulate(parameters, simulation_functions)
