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
from time import time

import ragaraja, register_machine
import dose_world

from simulation_calls import spawn_populations, eco_cell_iterator, deploy
from simulation_calls import interpret_chromosome, step, report_generation
from simulation_calls import bury_world, write_parameters, close_results

from database_calls import prepare_database, db_log_simulation_parameters
from database_calls import db_report

class dose_functions():
    '''
    Abstract class to contain all of the simulation-specific functions 
    (functions that vary with each simulation) that are to be defined / 
    implemented by the user to be used in a simulation. This class should 
    be inherited by every simulation to over-ride each function / method. 
    
    This set of functions / methods is consolidated functions / methods to 
    be over-ridden from genetic.Organism, genetic.Population, and 
    dose_world.World classes. As a result, the functions / methods can be
    working at different levels - at the level of individual organisms, 
    at the level of entire population(s), or at the level of the world.
    
    Please see the examples in examples directory on its use.
    '''
    def mutation_scheme(self, organism):
        '''
        Method / function to trigger mutational events in each chromosome 
        of the genome within an organism. This function works at the 
        level of individual organisms.
        
        @param organism: genetic.Organism object
        @return: None
        '''
        raise NotImplementedError
    def prepopulation_control(self, Populations, pop_name):
        '''
        Method / function to trigger population control events before 
        mating event in each generation. For example, it can be used to
        simulate pre-puberty (childhood) death. This function works at 
        the level of entire population(s).
        
        @param Population: A dictionary containing one or more populations 
        where the value is a genetic.Population object.
        @param pop_name: Name of the population which is used as key in 
        the the dictionary (Populations parameter).
        @return: None
        '''
        raise NotImplementedError
    def fitness(self, Populations, pop_name):
        '''
        Method / function to calculate the fitness score of each organism 
        within the population(s). This function works at the level of 
        entire population(s) even though fitness calculation occurs at the 
        organism level. The fitness of each organism may be stored in 
        Organism.status['fitness'] and may be used by mating scheme.
        
        @param Population: A dictionary containing one or more populations 
        where the value is a genetic.Population object.
        @param pop_name: Name of the population which is used as key in 
        the the dictionary (Populations parameter).
        @return: None
        '''
        raise NotImplementedError
    def mating(self, Populations, pop_name):
        '''
        Method / function to trigger mating events in each generation. For 
        example, it can be used to simulates mate choices and progeny size. 
        A support function provided is genetic.crossover() function which 
        generates one random crossover operation between 2 chromosomes, to 
        simulate meiosis crossover. This function may also use one or more 
        of the dose.filter_XXX() functions to select or choose suitable 
        mates. This function works at the level of entire population(s), 
        which means that this function will have 
        - to manage mating scheme and progeny (offspring) generation for 
        the entire population
        - add or replace offsprings into the respective population(s)
        
        @param Population: A dictionary containing one or more populations 
        where the value is a genetic.Population object.
        @param pop_name: Name of the population which is used as key in 
        the the dictionary (Populations parameter).
        @return: None
        '''
        raise NotImplementedError
    def postpopulation_control(self, Populations, pop_name):
        '''
        Method / function to trigger population control events after 
        mating event in each generation. For example, it can be used to
        simulate old-age death. This function works at the level of entire 
        population(s).
        
        @param Population: A dictionary containing one or more populations 
        where the value is a genetic.Population object.
        @param pop_name: Name of the population which is used as key in 
        the the dictionary (Populations parameter).
        @return: None
        '''
        raise NotImplementedError
    def generation_events(self, Populations, pop_name):
        '''
        Method / function to trigger other defined events in each 
        generation. For example, it can be used to simulate catastrophe 
        or epidemic that does not occur regularly, or simulates unusual 
        occurrences of multiple mutation events. This function works at 
        the level of entire population(s).
        
        @param Population: A dictionary containing one or more populations 
        where the value is a genetic.Population object.
        @param pop_name: Name of the population which is used as key in 
        the the dictionary (Populations parameter).
        @return: None
        '''
        raise NotImplementedError
    def population_report(self, Populations, pop_name):
        '''
        Method / function to generate a text report of the population(s) 
        and/or each organisms within the population at regular intervals, 
        within the simulation, as determined by "print_frequency" in the 
        simulation parameters. This function works at the level of entire 
        population(s).
        
        @param Population: A dictionary containing one or more populations 
        where the value is a genetic.Population object.
        @param pop_name: Name of the population which is used as key in 
        the the dictionary (Populations parameter).
        @return: Entire report of a population at a generation count in a 
        string. To make it human-readable, usually the report string is 
        both tab-delimited (for one organism) and newline-delimited (for 
        entire population). 
        '''
        raise NotImplementedError
    def organism_movement(self, Populations, pop_name, World):
        '''
        organism_movement and organism_location are both methods / 
        functions to execute movement of organisms within the world. The 
        semantic difference between organism_movement and organism_location 
        is that organism_movement is generally used for short travels 
        while organism_location is used for long travel. For example, 
        organism_movement can be used to simulate foraging or nomadic
        behaviour. This function works at both the level of entire 
        population(s) and world.
        
        For each organism to move, this function will have to 
        - update the number of organisms in each 
        World.ecosystem[x-axis][y-axis][z-axis]['organisms']
        - update the respective Organism's location in the status 
        dictionary (Population[pop_name].agents[<index>].status['location'])
        
        @param Population: A dictionary containing one or more populations 
        where the value is a genetic.Population object.
        @param pop_name: Name of the population which is used as key in 
        the the dictionary (Populations parameter).
        @param World: dose_world.World object.
        @return: None
        '''
        raise NotImplementedError
    def organism_location(self, Populations, pop_name, World):
        '''
        organism_movement and organism_location are both methods / 
        functions to execute movement of organisms within the world. The 
        semantic difference between organism_movement and organism_location 
        is that organism_movement is generally used for short travels 
        while organism_location is used for long travel. For example, 
        organism_movement can be used to simulate long distance migration, 
        such as air travel. This function works at both the level of entire 
        population(s) and world.
        
        For each organism to move, this function will have to 
        - update the number of organisms in each 
        World.ecosystem[x-axis][y-axis][z-axis]['organisms']
        - update the respective Organism's location in the status 
        dictionary (Population[pop_name].agents[<index>].status['location'])
        
        @param Population: A dictionary containing one or more populations 
        where the value is a genetic.Population object.
        @param pop_name: Name of the population which is used as key in 
        the the dictionary (Populations parameter).
        @param World: dose_world.World object.
        @return: None
        '''
        raise NotImplementedError
    def ecoregulate(self, World): 
        '''
        Method / function for broad spectrum management of the entire 
        ecosystem defined as World.ecosystem[x-axis][y-axis][z-axis]
        ['local_input'] and World.ecosystem[x-axis][y-axis][z-axis]
        ['local_output']). For example, it can be used to simulate 
        temperature, solar radiation, or resource gradients. This function 
        works at the level of the world.
        
        @param World: dose_world.World object.
        @return: None
        '''
        raise NotImplementedError
    def update_ecology(self, World, x, y, z):
        '''
        Method / function to process the input and output from the 
        activities of the organisms in the current ecological cell (defined 
        as World.ecosystem[x-axis][y-axis][z-axis]['temporary_input'] and 
        World.ecosystem[x-axis][y-axis][z-axis]['temporary_output']) into 
        a local ecological cell condition (defined as World.ecosystem
        [x-axis][y-axis][z-axis]['local_input'] and World.ecosystem[x-axis]
        [y-axis][z-axis]['local_output']), and update the
        ecosystem (which is essentially the ecological cell adjacent to 
        World.ecosystem[x-axis][y-axis][z-axis]). For example, it can be 
        used to simulate secretion of chemicals or use of resources (such 
        as food) by organisms, and diffusion of secretions to the 
        neighbouring ecological cells. 
        
        Essentially, this function simulates the "diffusion" of local 
        situation outwards. This function works at the level of the world.
        
        @param World: dose_world.World object.
        @param x: x-axis of the World.ecosystem to identify the cell.
        @param y: y-axis of the World.ecosystem to identify the cell.
        @param z: z-axis of the World.ecosystem to identify the cell.
        @return: None
        '''
        raise NotImplementedError
    def update_local(self, World, x, y, z):
        '''
        Method / function to update local ecological cell condition (defined 
        as World.ecosystem[x-axis][y-axis][z-axis]['local_input'] and 
        World.ecosystem[x-axis][y-axis][z-axis]['local_output']) from the 
        ecosystem (World.ecosystem [x-axis][y-axis][z-axis]['local_input'] 
        and World.ecosystem[x-axis][y-axis][z-axis]['local_output'] of 
        adjacent ecological cells). For example, it can be used to 
        simulates movement or diffusion of resources from the ecosystem to 
        local. 
        
        Essentially, this function is the reverse of update_ecology() 
        function. In this case, the local ecological cell is affected by 
        adjacent conditions. This function works at the level of the world.
        
        @param World: dose_world.World object.
        @param x: x-axis of the World.ecosystem to identify the cell.
        @param y: y-axis of the World.ecosystem to identify the cell.
        @param z: z-axis of the World.ecosystem to identify the cell.
        @return: None
        '''
        raise NotImplementedError
    def report(self, World):
        '''
        Method / function to generate a text report of the population(s) 
        and/or each organisms within the population at regular intervals, 
        within the simulation, as determined by "print_frequency" in the 
        simulation parameters. This function works at the level of world.
        
        @param World: dose_world.World object.
        @return: Entire report of a population at a generation count in a 
        string. To make it human-readable, usually the report string is 
        both tab-delimited (for one organism) and newline-delimited (for 
        entire population). 
        '''
        raise NotImplementedError
    def deployment_scheme(self, Populations, pop_name, World):
        '''
        Method / function to implement a user-specific / simulation-
        specific deployment scheme used to deploy organisms into the 
        World. This function will only be used when "deployment_code" in 
        simulation parameters dictionary equals to 0. This function works 
        at all three levels - organism(s), population(s), and world.
        
        @param Population: A dictionary containing one or more populations 
        where the value is a genetic.Population object.
        @param pop_name: Name of the population which is used as key in 
        the the dictionary (Populations parameter).
        @param World: dose_world.World object.
        @return: None
        '''
        raise NotImplementedError
    def database_report(self, con, cur, start_time,
                        Population, World, generation_count):
        '''
        Method / function to implement database logging of each organism 
        in each population, and the ecosystem status. The frequency of 
        logging is determined by "database_logging_frequency" in the 
        simulation_parameters.
        
        Three database tables had been defined for use in this function:
        - organisms where the structure is (start_time text, pop_name text, 
            org_name text, generation text, key text, value text)
        - world where the structure is (start_time text, x text, y text, 
            z text, generation text, key text, value text)
        - miscellaneous where the structure is (start_time text, 
            generation text, key text, value text)
            
        The logical purpose of these tables are:
        - organisms, to log status of each organism. Starting time of 
            current simulation (start_time), population name (pop_name), 
            organism name (org_name), and generation count (generation) 
            are used as complex primary key to identify the organism 
            within a specific simulation at a specific generation. Key and 
            value pair makes up the actual data to be logged where key is 
            the field and value is the datum or attribute.
        - world, to log the status of the ecosystem. Starting time of 
            current simulation (start_time), location of ecological cell 
            (x, y, z as coordinates), and generation count (generation) 
            are used as complex primary key to identify the ecological cell
            within a specific simulation at a specific generation. Key and 
            value pair makes up the actual data to be logged where key is 
            the field and value is the datum or attribute.
        - miscellaneous, is used to log other undefined data. Starting 
            time of current simulation (start_time), and generation count 
            (generation) are used as complex primary key to identify a 
            specific generation within a specific simulation. Key and 
            value pair makes up the actual data to be logged where key is 
            the field and value is the datum or attribute.
        
        @param con: Database connector. See Python DB-API for details.
        @param cur: Database cursor. See Python DB-API for details.
        @param start_time: Starting time of current simulation in the 
        format of <date>-<seconds since epoch>; for example, 
        2013-10-11-1381480985.77.
        @param Population: A dictionary containing one or more populations 
        where the value is a genetic.Population object.
        @param World: dose_world.World object.
        @param generation_count: Current number of generations simulated.
        @return: None
        '''
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
    # time_start format = <date>-<seconds since epoch>
    # for example, 2013-10-11-1381480985.77
    time_start = '-'.join([str(datetime.utcnow()).split(' ')[0], 
                           str(time())])
    # Directory to store simulation results is in the format of
    # <CWD>/Simulations/<simulation name>_<date>-<seconds since epoch>/
    # eg. <CWD>/Simulations/01_basic_functions_one_cell_deployment_2013-10-11-1381480985.77/
    directory = '_'.join([sim_parameters["simulation_name"], time_start])
    directory = os.sep.join([os.getcwd(), 'Simulations', directory]) 
    directory = directory + os.sep
    if not os.path.exists(directory):
        os.makedirs(directory)
    sim_parameters.update(
        {"initial_chromosome":['0'] * sim_parameters["chromosome_size"],
         "deployment_scheme": sim_functions.deployment_scheme,
         "starting_time": time_start,
         "directory": directory})
    if sim_parameters.has_key("database_file") and \
        sim_parameters.has_key("database_logging_frequency"): 
        (con, cur) = prepare_database(sim_parameters)
        (con, cur) = db_log_simulation_parameters(con, cur, sim_parameters)
    Populations = spawn_populations(sim_parameters)
    ragaraja.activate_version(sim_parameters["ragaraja_version"])
    for pop_name in Populations:
        write_parameters(sim_parameters, pop_name)
        deploy(sim_parameters, Populations, pop_name, World)          
    generation_count = 0
    while generation_count < sim_parameters["maximum_generations"]:
        generation_count = generation_count + 1
        sim_functions.ecoregulate(World)
        eco_cell_iterator(World, sim_parameters, 
                          sim_functions.update_ecology)
        eco_cell_iterator(World, sim_parameters, 
                          sim_functions.update_local)
        interpret_chromosome(sim_parameters, Populations, 
                             pop_name, World)
        report_generation(sim_parameters, Populations, pop_name, 
                          sim_functions, generation_count)
        sim_functions.organism_movement(Populations, pop_name, World)
        sim_functions.organism_location(Populations, pop_name, World)
        eco_cell_iterator(World, sim_parameters, sim_functions.report)
        bury_world(sim_parameters, World, generation_count)
        if sim_parameters.has_key("database_file") and \
            sim_parameters.has_key("database_logging_frequency") and \
            generation_count % int(sim_parameters["database_logging_frequency"]) == 0: 
            (con, cur) = db_report(con, cur, sim_functions, time_start,
                                   Populations, World, generation_count)
    close_results(sim_parameters, pop_name)
    if sim_parameters.has_key("database_file") and \
        sim_parameters.has_key("database_logging_frequency"): 
        con.commit()
        con.close()
            
