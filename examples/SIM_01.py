# needed to run this example without prior
# installation of DOSE into Python site-packages
import run_examples_without_installation

# Example codes starts from here
import dose

parameters = {
              "simulation_code": "SIM_01",
              "population_names": ['pop_01','pop_02'],
              "population_locations": [[(0,0,0), (1,1,1), (2,2,2)], [(4,4,4), (3,3,3), (2,2,2)]],
              "deployment_code": 3,
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
              "population_size": 100,
              "eco_cell_capacity": 50,
              "world_x": 5,
              "world_y": 5,
              "world_z": 5,
              "goal": 0,
              "maximum_generations": 100,
              "fossilized_ratio": 0.01,
              "fossilized_frequency": 20,
              "print_frequency": 10,
              "ragaraja_version": 2,
              "eco_buried_frequency": 100,
             }

class simulation_functions(dose.dose_functions):

    def organism_movement(self, x, y, z): pass

    def organism_location(self, x, y, z): pass

    def ecoregulate(self): pass

    def update_ecology(self, x, y, z): pass

    def update_local(self, x, y, z): pass

    def report(self): pass

    def fitness(self): pass

    def mutation_scheme(self, organism): 
        organism.genome[0].rmutate(parameters["mutation_type"],
                                   parameters["additional_mutation"])

    def prepopulation_control(self): pass

    def mating(self): pass

    def postpopulation_control(self): pass

    def generation_events(self): pass

    def population_report(self, Populations, population):
        sequences = [''.join(org.genome[0].sequence) for org in Populations[population].agents]
        identities = [org.status['identity'] for org in Populations[population].agents]
        locations = [str(org.status['location']) for org in Populations[population].agents]
        demes = [org.status['deme'] for org in Populations[population].agents]
        return '\n'.join(identities)

    def deployment_scheme(self, Populations, World, pop_name): pass

dose.simulate(parameters, simulation_functions)
