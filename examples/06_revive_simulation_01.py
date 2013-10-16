# needed to run this example without prior
# installation of DOSE into Python site-packages
import run_examples_without_installation

# Example codes starts from here
import dose
import os

simulation_folder = '01_basic_functions_one_cell_deployment_2013-10-13-1381664013.83'
simulation_folder = os.sep.join([os.getcwd(), 'Simulations', simulation_folder]) + os.sep

rev_parameters = {"sim_folder" : simulation_folder,
                  "eco_file" : '01_basic_functions_one_cell_deployment_gen100.eco', 
                  "pop_files" : ['01_basic_functions_one_cell_deployment_pop_01_pop100_100.gap'],
                  "extend_gen" : 30,
                  "simulation_name": "06_revive_simulation_01",
                  "population_names": ['pop_01'],
                  "chromosome_bases": ['0','1'],
                  "background_mutation": 0.1,
                  "additional_mutation": 0,
                  "mutation_type": 'point',
                  "cells": 50,
                  "tape_length": 200,
                  "clean_cell": True,
                  "interpret_chromosome": True,
                  "max_codon": 2000,
                  "goal": 0,
                  "eco_cell_capacity": 100,
                  "fossilized_ratio": 0.01,
                  "fossilized_frequency": 20,
                  "print_frequency": 10,
                  "ragaraja_version": 0,
                  "ragaraja_instructions": ['000', '001', '010',
                                            '011', '100', '101'],
                  "eco_buried_frequency": 100,
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
        organism.genome[0].rmutate(rev_parameters["mutation_type"],
                                   rev_parameters["additional_mutation"])

    def prepopulation_control(self, Populations, pop_name): pass

    def mating(self, Populations, pop_name): pass

    def postpopulation_control(self, Populations, pop_name): pass

    def generation_events(self, Populations, pop_name): pass

    def population_report(self, Populations, pop_name):
        sequences = [''.join(org.genome[0].sequence) for org in Populations[pop_name].agents]
        identities = [org.status['identity'] for org in Populations[pop_name].agents]
        locations = [str(org.status['location']) for org in Populations[pop_name].agents]
        demes = [org.status['deme'] for org in Populations[pop_name].agents]
        return '\n'.join(sequences)

    def database_report(self, con, cur, start_time, 
                        Populations, World, generation_count):
        dose.database_report_populations(con, cur, start_time, 
                                         Populations, generation_count)
        dose.database_report_world(con, cur, start_time, 
                                   World, generation_count)

    def deployment_scheme(self, Populations, pop_name, World): pass

dose.revive_simulation(rev_parameters, simulation_functions)

