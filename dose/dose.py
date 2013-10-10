'''
Application Programming Interface (API) for DOSE (digital organism 
simulation environment). This contains the main functions and operations 
needed to write a DOSE simulation. This file will be imported as top 
level (from dose import *) when DOSE is imported; hence, all functions in 
this file can be assessed at top level.

Date created: 27th September 2013
'''
import sys, os, random, inspect
from datetime import datetime

import ragaraja, register_machine
import dose_world

from simulation_calls import spawn_populations, eco_cell_iterator, deploy
from simulation_calls import interpret_chromosome, step, report_generation
from simulation_calls import bury_world, write_parameters, close_results

class dose_functions():
    def organism_movement(self, Populations, pop_name, World):
        raise NotImplementedError
    def organism_location(self, Populations, pop_name, World):
        raise NotImplementedError
    def ecoregulate(self, World): 
        raise NotImplementedError
    def update_ecology(self, World, x, y, z):
        raise NotImplementedError
    def update_local(self, World, x, y, z):
        raise NotImplementedError
    def report(World):
        raise NotImplementedError
    def fitness(self, Populations, pop_name):
        raise NotImplementedError
    def mutation_scheme(self, organism):
        raise NotImplementedError
    def prepopulation_control(self, Populations, pop_name):
        raise NotImplementedError
    def mating(self, Populations, pop_name):
        raise NotImplementedError
    def postpopulation_control(self, Populations, pop_name):
        raise NotImplementedError
    def generation_events(self, Populations, pop_name):
        raise NotImplementedError
    def population_report(self, Populations, pop_name):
        raise NotImplementedError
    def deployment_scheme(Populations, pop_name, World):
        raise NotImplementedError

def filter_deme(deme_name, agents):
    extract = []
    for individual in agents:
        if individual.status['deme'].upper() == deme_name.upper():
            extract.append(individual)
    return extract
    
def filter_gender(gender, agents):
    extract = []
    for individual in agents:
        if individual.status['gender'].upper() == gender.upper():
            extract.append(individual)
    return extract

def filter_age(minimum, maximum, agents):
    extract = []
    for individual in agents:
        if float(individual.status['age']) > (float(minimum) - 0.01):
            if float(individual.status['age']) < float(maximum) + 0.01:
                extract.append(individual)
    return extract

def filter_location(location, agents):
    extract = []
    for individual in agents:
        if individual.status['location'] == location:
            extract.append(individual)
    return extract

def filter_vitality(minimum, maximum, agents):
    extract = []
    for individual in agents:
        if float(individual.status['vitality']) > (float(minimum) - 0.01):
            if float(individual.status['vitality']) < float(maximum) + 0.01:
                extract.append(individual)
    return extract

def filter_status(status_key, condition, agents):
    extract = []
    for individual in agents:
        if type(condition) in (str, int, float, bool):
            if individual.status[status_key] == condition:
                extract.append(individual)
        elif float(individual.status[status_key]) > float(condition[0]) - 0.01:
            if float(individual.status[status_key]) < float(condition[1]) + 0.01:
                extract.append(individual)
    return extract

def simulate(sim_parameters, simulation_functions):
    sim_functions = simulation_functions()
    World = dose_world.World(sim_parameters["world_x"],
                             sim_parameters["world_y"],
                             sim_parameters["world_z"])
    time_start = str(datetime.utcnow())
    directory = "%s\\Simulations\\%s_%s\\" % (os.getcwd(), 
                                              sim_parameters["simulation_name"], 
                                              time_start[0:10])
    if not os.path.exists(directory):
        os.makedirs(directory)
    sim_parameters.update({"initial_chromosome":['0'] * sim_parameters["chromosome_size"],
                           "deployment_scheme": sim_functions.deployment_scheme,
                           "starting_time": time_start,
                           "directory": directory})
    Populations = spawn_populations(sim_parameters)
    ragaraja.activate_version(sim_parameters["ragaraja_version"])
    for pop_name in Populations:
        write_parameters(sim_parameters, pop_name)
        deploy(sim_parameters, Populations, pop_name, World)          
        generation_count = 0
        while generation_count < sim_parameters["maximum_generations"]:
            generation_count = generation_count + 1
            sim_functions.ecoregulate(World)
            eco_cell_iterator(World, sim_parameters, sim_functions.update_ecology)
            eco_cell_iterator(World, sim_parameters, sim_functions.update_local)
            interpret_chromosome(sim_parameters, Populations, pop_name, World)
            report_generation(sim_parameters, Populations, pop_name, sim_functions, generation_count)
            sim_functions.organism_movement(Populations, pop_name, World)
            sim_functions.organism_location(Populations, pop_name, World)
            eco_cell_iterator(World, sim_parameters, sim_functions.report)
            bury_world(sim_parameters, World, generation_count)
        close_results(sim_parameters, pop_name)
