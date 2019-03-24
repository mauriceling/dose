'''
File containing support functions for running a simulation. The functions 
in this file is not for public use; all functions in this file are private 
functions.

Date created: 10th October 2013
'''
import random, inspect, os
import os.path
from datetime import datetime
from time import time
from copy import deepcopy
from shutil import copyfile

# In Python 3, cPickle is no longer needed: Py3 looks for
# an optimized version, and if it founds none, will load the
# pure python implementation of pickle. 
try:
    import cPickle as pickle
except ImportError:
    import pickle

from . import dose_world
from . import genetic
from . import ragaraja, register_machine

from .database_calls import connect_database, db_log_simulation_parameters
from .database_calls import db_report

def simulation_core(sim_functions, sim_parameters, Populations, World):
    '''
    Sequential ecological cell DOSE simulator.
    
    Performs the following operations:
        - Creating simulation file directory for results text file, population 
        freeze, and world burial storage
        - Generate a simulation start time to identify the current simulation
        - Define active Ragaraja instructions
        - Connecting to logging database (if needed)
        - Writing simulation parameters into results text file
        - Initialize World and Population
        - Deploy population(s) onto the world
        - Run the simulation and recording the results
        - Writing final results into results text file
        - Close logging database (if used)
        - Copy simulation script into simulation file directory
    
    @param sim_functions: implemented simulation functions (see 
    dose.dose_functions)
    @param sim_parameters: simulation parameters dictionary (see Examples)
    @param Populations: dictionary of population objects
    @param World: dose_world.World object
    '''
    time_start = '-'.join([str(datetime.utcnow()).split(' ')[0],
                           str(time())])
    print('Creating simulation file directories...')
    directory ='_'.join([sim_parameters["simulation_name"],time_start])
    directory = os.sep.join([os.getcwd(), 'Simulations', directory]) 
    directory = directory + os.sep
    if not os.path.exists(directory): os.makedirs(directory)
    print('Adding simulation directory to simulation parameters...')
    sim_parameters["directory"] = directory
    print('Adding starting time to simulation parameters...')
    sim_parameters["starting_time"] = time_start
    sim_functions = sim_functions()
    if sim_parameters["ragaraja_version"] == 0:
        print('Activating ragaraja version: 0...')
        ragaraja.activate_version(sim_parameters["ragaraja_version"],
                                  sim_parameters["ragaraja_instructions"])
    else:
        print('Activating ragaraja version: ' + \
            str(sim_parameters["ragaraja_version"]) + '...')
        ragaraja.activate_version(sim_parameters["ragaraja_version"])
    if "database_file" in sim_parameters and \
        "database_logging_frequency" in sim_parameters: 
        print('Connecting to database file: ' + \
            sim_parameters["database_file"] + '...')
        (con, cur) = connect_database(None, sim_parameters)
        print('Logging simulation parameters to database file...')
        (con, cur) = db_log_simulation_parameters(con, cur, sim_parameters)
    for pop_name in Populations:
        print('\nPreparing population: ' + pop_name + ' for simulation...')
        if 'sim_folder' in sim_parameters or \
            'database_source' in sim_parameters:
            print('Calculating final generation count...')
            max = sim_parameters["rev_start"] \
                [sim_parameters["population_names"].index(pop_name)] + \
                sim_parameters["extend_gen"]
            print('Updating generation count from previous simulation...')
            generation_count = sim_parameters["rev_start"][0]
        else:
            print('Deploying population in World entity...')
            if sim_parameters["deployment_code"] == 0:
                print('Executing user defined deployment scheme...')
                deploy_0(sim_parameters, Populations, pop_name, World)      
            elif sim_parameters["deployment_code"] == 1:
                print('Executing deployment code 1: Single eco-cell deployment...')
                deploy_1(sim_parameters, Populations, pop_name, World)  
            elif sim_parameters["deployment_code"] == 2:
                print('Executing deployment code 2: Random eco-cell deployment...')
                deploy_2(sim_parameters, Populations, pop_name, World)  
            elif sim_parameters["deployment_code"] == 3:
                print('Executing deployment code 3: Even eco-cell deployment...')
                deploy_3(sim_parameters, Populations, pop_name, World)  
            elif sim_parameters["deployment_code"] == 4:
                print('Executing deployment code 4: Centralized eco-cell deployment...')
                deploy_4(sim_parameters, Populations, pop_name, World)
            print('Adding maximum generations to simulation parameters...')
            max = sim_parameters["maximum_generations"]
            generation_count = 0
        print('Writing simulation parameters into txt file report...')
        write_parameters(sim_parameters, pop_name)
        print('Updating generation count...')
        Populations[pop_name].generation = generation_count
    print('\nSimulation preparation complete...')
    while generation_count < max:
        generation_count = generation_count + 1
        sim_functions.ecoregulate(World)
        eco_cell_iterator(World, sim_parameters,
                          sim_functions.update_ecology)
        eco_cell_iterator(World, sim_parameters,
                          sim_functions.update_local)
        eco_cell_iterator(World, sim_parameters, sim_functions.report)
        bury_world(sim_parameters, World, generation_count)
        for pop_name in Populations:
            if sim_parameters["interpret_chromosome"]:
                interpret_chromosome(sim_parameters, Populations, 
                                     pop_name, World)
            report_generation(sim_parameters, Populations, pop_name, 
                              sim_functions, generation_count)
            sim_functions.organism_movement(Populations, pop_name, World)
            sim_functions.organism_location(Populations, pop_name, World)
        if "database_file" in sim_parameters and \
            "database_logging_frequency" in sim_parameters and \
            generation_count % \
            int(sim_parameters["database_logging_frequency"]) == 0: 
                (con, cur) = db_report(con, cur, sim_functions,
                                   sim_parameters["starting_time"],
                                   Populations, World, generation_count)
        print('Generation ' + str(generation_count) + ' complete...')
    print('\nClosing simulation results...')
    for pop_name in Populations: close_results(sim_parameters, pop_name)
    if "database_file" in sim_parameters and \
        "database_logging_frequency" in sim_parameters:
        print('Committing logged data into database file...') 
        con.commit()
        print('Terminating database connection...') 
        con.close()
    print('Copying simulation file script to simulation results directory...')

    #DV on my system, the inspect.stack()[2][1] value returns the full
    #   path to the file ('/home/douwe/scr/.../scriptname.py'). 
    #   The end result is an error for the original code, below, as the 
    #   copyfile command is pointed to a wrong location: the directory
    #   is added twice. This might be Py3, or Windows functionality.
    #   With using the os.path module, this should give an OS-independent
    #   way of extracting the basename and linking to the directory.
    sim_script_basename = os.path.basename(inspect.stack()[2][1])
    copyfile(inspect.stack()[2][1], 
#DV_original#             sim_parameters['directory'] + inspect.stack()[2][1])
             os.path.join(sim_parameters['directory'], sim_script_basename))
    print('\nSimulation ended...')

def coordinates(location):
    '''
    Helper function to transpose ecological cell into a tuple.
    
    @param location: location of ecological cell as 3-element iterable 
    data type
    @return: location of ecological cell as (x,y,z)
    '''
    x = location[0]
    y = location[1]
    z = location[2]
    return (x,y,z)

def adjacent_cells(sim_parameters, location):
    '''
    Function to get a list of adjacent ecological cells from a given 
    location.
    
    @param sim_parameters: simulation parameters dictionary (see Examples)
    @param location: location of ecological cell as (x,y,z)
    @return: list of locations of adjacent cells.
    '''
    trashbin = []
    temp_cells = []
    world_size = [sim_parameters["world_x"],
                  sim_parameters["world_y"],
                  sim_parameters["world_z"]]
    for i in range(3):
        new_location = [spot for spot in location]
        new_location[0] += 1
        temp_cells.append(new_location)
        new_location = [spot for spot in location]
        new_location[0] -= 1
        temp_cells.append(new_location)    
    for i in range(2):
        new_location = [spot for spot in location]
        new_location[1] -= 1
        temp_cells.append(new_location) 
    for i in range(0,4,3):
        temp_cells[i][1] += 1
        temp_cells[i+1][1] -= 1
    temp_cells[-1][1] += 2
    for i in range(8):
        for x in range(2):
            if temp_cells[i][x] >= world_size[x] or temp_cells[i][x] < 0:
                if temp_cells[i] not in trashbin:
                    trashbin.append(temp_cells[i])
    for location in trashbin:
        temp_cells.remove(location)
    return [tuple(location) for location in temp_cells]

def spawn_populations(sim_parameters):
    '''
    Initializing starting population(s) for a simulation. Each organism 
    in each population at this stage will be genetic clones of each 
    other.
    
    @param sim_parameters: simulation parameters dictionary (see Examples)
    @return: dictionary of population objects with population name as key
    '''
    temp_Populations = {}
    print(' - Accessing population names...')
    for pop_name in sim_parameters["population_names"]:
        print(' - Constructing population: ' + pop_name + '...')
        temp_Populations[pop_name] = \
            genetic.population_constructor(sim_parameters)
        print(' - Updating organism identity and deme status...')
        for individual in temp_Populations[pop_name].agents:
            individual.generate_name()
            individual.status['deme'] = pop_name
    return temp_Populations

def eco_cell_iterator(World, sim_parameters, function):
    '''
    Generic caller to call any function to be executed in each ecological 
    cell in sequence.
    
    @param World: dose_world.World object
    @param sim_parameters: simulation parameters dictionary (see Examples)
    @param function: function to be executed
    @return: none
    '''
    for x in range(sim_parameters["world_x"]):
        for y in range(sim_parameters["world_y"]):
            for z in range(sim_parameters["world_z"]):
                if len(inspect.getargspec(function)[0]) == 5:
                    function(World, x, y, z)
                else:
                    function(World)

def deploy_0(sim_parameters, Populations, pop_name, World):
    '''
    Organism deployment scheme 0 - User defined deployment scheme. This is 
    called when "deployment_code" in simulation parameters = 0. User will 
    have to provide a deployment scheme/function as "deployment_scheme" in 
    simulation parameters.
    
    @param sim_parameters: simulation parameters dictionary (see Examples)
    @param Populations: dictionary of population objects
    @param pop_name: population name
    @param World: dose_world.World object
    @return: none.
    '''
    sim_parameters["deployment_scheme"](Populations, pop_name, World)

def deploy_1(sim_parameters, Populations, pop_name, World):
    '''
    Organism deployment scheme 1 - Single ecological cell deployment 
    scheme. This is called when "deployment_code" in simulation parameters 
    = 1. In this scheme, all organisms in the specified population 
    (specified by population name) will be deployed in the ecological cell 
    specified in "population_locations" of simulation parameters.
    
    @param sim_parameters: simulation parameters dictionary (see Examples)
    @param Populations: dictionary of population objects
    @param pop_name: population name
    @param World: dose_world.World object
    @return: none.
    '''
    position = sim_parameters["population_names"].index(pop_name)
    locations = [location 
        for location in sim_parameters["population_locations"][position]]
    (x,y,z) = coordinates(locations[0])
    World.ecosystem[x][y][z]['organisms'] = sim_parameters["population_size"]
    for individual in Populations[pop_name].agents:
        individual.status['location'] = locations[0]

def deploy_2(sim_parameters, Populations, pop_name, World):
    '''
    Organism deployment scheme 2 - Random deployment scheme. This is called 
    when "deployment_code" in simulation parameters = 2. In this scheme, 
    all organisms in the specified population (specified by population 
    name) will be randomly deployed across the list of ecological cells 
    specified as "population_locations" of simulation parameters.
    
    @param sim_parameters: simulation parameters dictionary (see Examples)
    @param Populations: dictionary of population objects
    @param pop_name: population name
    @param World: dose_world.World object
    @return: none
    '''
    position = sim_parameters["population_names"].index(pop_name)
    locations = [location 
        for location in sim_parameters["population_locations"][position]]
    for individual in Populations[pop_name].agents:
            location = random.choice(locations)
            (x,y,z) = coordinates(location)
            while World.ecosystem[x][y][z]['organisms'] >= \
                sim_parameters["eco_cell_capacity"]:
                location = random.choice(locations)
                (x,y,z) = coordinates(location)
            World.ecosystem[x][y][z]['organisms'] = \
                World.ecosystem[x][y][z]['organisms'] + 1
            individual.status['location'] = location

def deploy_3(sim_parameters, Populations, pop_name, World):
    '''
    Organism deployment scheme 3 - Even deployment scheme. This is called 
    when "deployment_code" in simulation parameters = 3. In this scheme, 
    all organisms in the specified population (specified by population 
    name) will be evenly deployed (as much as possible) across the list of 
    ecological cells specified as "population_locations" of simulation 
    parameters.
    
    @param sim_parameters: simulation parameters dictionary (see Examples)
    @param Populations: dictionary of population objects
    @param pop_name: population name
    @param World: dose_world.World object
    @return: none
    '''
    position = sim_parameters["population_names"].index(pop_name)
    locations = [location 
        for location in sim_parameters["population_locations"][position]]
    iterator = 0
    for i in range(sim_parameters["population_size"]):
        individual = Populations[pop_name].agents[i]
        location = locations[iterator]
        (x,y,z) = coordinates(location)
        World.ecosystem[x][y][z]['organisms'] = \
            World.ecosystem[x][y][z]['organisms'] + 1
        individual.status['location'] = location
        iterator += 1
        if iterator == len(locations):
            iterator = 0

def deploy_4(sim_parameters, Populations, pop_name, World):
    '''
    Organism deployment scheme 4 - Centralized deployment scheme. This is 
    called when "deployment_code" in simulation parameters = 4. In this 
    scheme, all organisms in the specified population (specified by 
    population name) will be deployed onto the ecological cell specified 
    in "population_locations" of simulation parameters, up to the organism 
    capacity of the ecological cell (specified in "eco_cell_capacity" of 
    simulation parameters). In event that the specified deployment 
    locations is filled, undeployed organisms will be randomly deployed 
    onto adjacent cells.
    
    @param sim_parameters: simulation parameters dictionary (see Examples)
    @param Populations: dictionary of population objects
    @param pop_name: population name
    @param World: dose_world.World object
    @return: none
    '''
    position = sim_parameters["population_names"].index(pop_name)
    locations = [location 
        for location in sim_parameters["population_locations"][position]]
    adj_cells = adjacent_cells(sim_parameters, locations[0])
    for group in range((sim_parameters["population_size"] / \
                         sim_parameters["eco_cell_capacity"]) + 1):
        start = sim_parameters["eco_cell_capacity"] * group
        end = start + sim_parameters["eco_cell_capacity"]
        for x in range(start,end):
            if x == sim_parameters["population_size"]: break
            individual = Populations[pop_name].agents[x]
            if x > (sim_parameters["eco_cell_capacity"] - 1):
                location = random.choice(adj_cells)
                (x,y,z) = coordinates(location)
                while World.ecosystem[x][y][z]['organisms'] > \
                    sim_parameters["eco_cell_capacity"]:
                    location = random.choice(adj_cells)
                    (x,y,z) = coordinates(random.choice(adj_cells))
            (x,y,z) = coordinates(location)
            World.ecosystem[x][y][z]['organisms'] += 1
            individual.status['location'] = location

def interpret_chromosome(sim_parameters, Populations, pop_name, World):
    '''
    Function to call Ragaraja interpreter to express / execute the genome 
    for each organism in a population. The Turing tape (array) after 
    execution will be logged as "blood" of each organism. Ragaraja 
    interpreter will use the temporary_input and temporary_output lists 
    from each ecological cell as the input data and output data respectively 
    for genome execution - this will resemble consumption of environmental 
    resources and replenishing of environmental resources or dumping of 
    wastes respectively.
    
    @param sim_parameters: simulation parameters dictionary (see Examples)
    @param Populations: dictionary of population objects
    @param pop_name: population name
    @param World: dose_world.World object
    @return: none
    '''
    array = [0] * sim_parameters["max_tape_length"]
    for i in range(len(Populations[pop_name].agents)):
        individual = Populations[pop_name].agents[i]
        location = individual.status['location']
        (x,y,z) = coordinates(location)
        if sim_parameters["clean_cell"]:
            array = [0] * sim_parameters["max_tape_length"]
        else:
            array = Populations[pop_name].agents[i].status['blood']
            if array == None: 
                array = [0] * sim_parameters["max_tape_length"]
        for chromosome_count in range(len(individual.genome)):
            inputdata = World.ecosystem[x][y][z]['local_input']
            output = World.ecosystem[x][y][z]['local_output']
            source = ''.join(individual.genome[chromosome_count].sequence)
            if sim_parameters["ragaraja_version"] == 0.2:
                source = ragaraja.nBF_to_Ragaraja(source)
            array = Populations[pop_name].agents[i].status['blood']
            try: (array, apointer, inputdata, output, source, spointer) = \
                register_machine.interpret(source, ragaraja.ragaraja, 3,
                                           inputdata, array,
                                           sim_parameters["max_tape_length"],
                                           sim_parameters["max_codon"])
            except Exception as e: 
                error_msg = '|'.join(['Error at Chromosome_' + \
                    str(chromosome_count), str(e)])
                Populations[pop_name].agents[i]. \
                    status['chromosome_error'] = error_msg
                Populations[pop_name].agents[i].status['blood'] = array
            Populations[pop_name].agents[i].status['blood'] = array
            World.ecosystem[x][y][z]['temporary_input'] = inputdata
            World.ecosystem[x][y][z]['temporary_output'] = output

def step(Populations, pop_name, sim_functions):
    '''
    Performs a generational step for a population
        - Prepopulation control
        - Mutations
        - Before mating fitness measurement
        - Mating
        - Postpopulation control
        - Generational events
        - After mating fitness measurement
        - Generate a textual report for the current generation
    
    @param Populations: dictionary of population objects
    @param pop_name: population name
    @param sim_functions: implemented simulation functions 
    (see dose.dose_functions)
    @return: report as a string
    '''
    if Populations[pop_name].generation > 0:
        sim_functions.prepopulation_control(Populations, pop_name)
    for organism in Populations[pop_name].agents:
        sim_functions.mutation_scheme(organism)
    sim_functions.fitness(Populations, pop_name)
    sim_functions.mating(Populations, pop_name)
    sim_functions.postpopulation_control(Populations, pop_name)
    sim_functions.generation_events(Populations, pop_name)
    Populations[pop_name].generation = Populations[pop_name].generation + 1
    sim_functions.fitness(Populations, pop_name)
    return sim_functions.population_report(Populations, pop_name)

def report_generation(sim_parameters, Populations, pop_name, 
                      sim_functions, generation_count):
    '''
    Performs a generational step (using step function) for a population 
    and writes out the resulting report into results text file.
    
    @param sim_parameters: simulation parameters dictionary (see Examples)
    @param Populations: dictionary of population objects
    @param pop_name: population name
    @param sim_functions: implemented simulation functions (see 
    dose.dose_functions)
    @param generation_count: current generation count for reporting
    @return: none
    '''
    report = step(Populations, pop_name, sim_functions)
    if generation_count % int(sim_parameters["fossilized_frequency"]) == 0:
        file = '%s%s_%s_' % (sim_parameters["directory"],
                             sim_parameters["simulation_name"], pop_name)
        freeze_population(file, sim_parameters["fossilized_ratio"], 
                          Populations, pop_name)
    if generation_count % int(sim_parameters["print_frequency"]) == 0:
        f = open(('%s%s_%s.result.txt' % (sim_parameters["directory"],
                                          sim_parameters["simulation_name"], 
                                          pop_name)), 'a')
        dtstamp = str(datetime.utcnow())
        f.write('\n'.join(['\n' + dtstamp, 'GENERATION: ' + \
                           str(generation_count), str(report)]))
        f.write('\n')
        f.close

def bury_world(sim_parameters, World, generation_count):
    '''
    Function to bury entire world into a file.
    
    @param sim_parameters: simulation parameters dictionary (see Examples)
    @param World: dose_world.World object
    @param generation_count: current generation count for file name generation
    '''
    if generation_count % int (sim_parameters["eco_buried_frequency"]) == 0:
       filename = '%s%s_gen%s.eco' % (sim_parameters["directory"], 
                                      sim_parameters["simulation_name"], 
                                      str(generation_count))
       f = open(filename, 'wb')
       pickle.dump(World, f)
       f.close()

def excavate_world(eco_file):
    '''
    Excavate buried world from file.
    
    @param eco_file: buried world file generated by bury_world function.
    @return: excavated dose_world.World object
    '''
    f = open(eco_file, 'rb')
    return pickle.load(f)

def freeze_population(file, proportion, Populations, pop_name):
    '''
    Function to freeze part or whole of the population into a file. If 
    the number of organisms is less than 101, the entire population will 
    be frozen.
    
    @param file: file name prefix
    @param proportion: proportion of the population to freeze
    @param Populations: dictionary of population objects
    @param pop_name: population name to freeze
    '''
    if proportion > 1.0: proportion = 1.0
    agents = Populations[pop_name].agents
    if len(agents) < 101 or len(agents) * proportion < 101:
        sample = deepcopy(Populations[pop_name])
    else:
        new_agents = [agents[random.randint(0, len(agents) - 1)]
                      for x in range(int(len(agents) * proportion))]
        sample = deepcopy(Populations[pop_name])
        sample.agents = new_agents
    name = ''.join([file, 'pop', str(Populations[pop_name].generation), 
                    '_', str(len(sample.agents)), '.gap'])
    f = open(name, 'wb')
    pickle.dump(sample, f)
    f.close()

def revive_population(gap_file):
    '''
    Revive population from a frozen population file.
    
    @param gap_file: frozen population file generated by freeze_population
    function.
    @return: revived population object
    '''
    f = open(gap_file, 'rb')
    return pickle.load(f)

def write_parameters(sim_parameters, pop_name):
    '''
    Function to write simulation parameters into results text file as 
    header.
    
    @param sim_parameters: simulation parameters dictionary (see Examples)
    @param pop_name: population name
    @return: none
    '''
    f = open(('%s%s_%s.result.txt' % (sim_parameters["directory"],
                                      sim_parameters["simulation_name"],
                                      pop_name)), 'a')
    f.write("""SIMULATION: %s

----------------------------------------------------------------------
""" % sim_parameters["simulation_name"])
    if ('database_source' in sim_parameters) or \
        ('sim_folder' in sim_parameters):
        f.write("SIMULATION REVIVAL STARTED: %s\n\n" % \
                sim_parameters["starting_time"])
    else:
        f.write("SIMULATION STARTED: %s\n\n" % \
                sim_parameters["starting_time"])
    for key in sim_parameters:
        if key not in ('deployment_scheme', 'directory', 'sim_folder'):
            f.write("%s : %s\n" % (key, sim_parameters[key]))
    f.write("""\n\nREPORT
----------------------------------------------------------------------
""")

def close_results(sim_parameters, pop_name):
    '''
    Function to write footer of results text file.
    
    @param sim_parameters: simulation parameters dictionary (see Examples)
    @param pop_name: population name
    @return: none
    '''
    f = open(('%s%s_%s.result.txt' % (sim_parameters["directory"],
                                      sim_parameters["simulation_name"], 
                                      pop_name)), 'a')
    f.write('''
----------------------------------------------------------------------
SIMULATION ENDED: ''' + str(datetime.utcnow()))
    f.close()
