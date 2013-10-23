'''
File containing support functions for running a simulation.

Date created: 10th October 2013
'''
import random, inspect, os, cPickle
from datetime import datetime
from time import time
from copy import deepcopy
from shutil import copyfile

import dose_world
import genetic
import ragaraja, register_machine

from database_calls import connect_database, db_log_simulation_parameters
from database_calls import db_report

def simulation_core(sim_functions, sim_parameters, Populations, World):
    time_start = '-'.join([str(datetime.utcnow()).split(' ')[0],
                           str(time())])
    directory ='_'.join([sim_parameters["simulation_name"],time_start])
    directory = os.sep.join([os.getcwd(), 'Simulations', directory]) 
    directory = directory + os.sep
    if not os.path.exists(directory): os.makedirs(directory)
    sim_parameters["directory"] = directory
    sim_parameters["starting_time"] = time_start
    sim_functions = sim_functions()
    if sim_parameters["ragaraja_version"] == 0:
        ragaraja.activate_version(sim_parameters["ragaraja_version"],
                                  sim_parameters["ragaraja_instructions"])
    else:
        ragaraja.activate_version(sim_parameters["ragaraja_version"])
    if sim_parameters.has_key("database_file") and \
        sim_parameters.has_key("database_logging_frequency"): 
        (con, cur) = connect_database(None, sim_parameters)
        (con, cur) = db_log_simulation_parameters(con, cur, sim_parameters)
    for pop_name in Populations:
        if 'sim_folder' in sim_parameters or \
            'database_source' in sim_parameters:
            max = sim_parameters["rev_start"][0] + sim_parameters["extend_gen"]
            generation_count = sim_parameters["rev_start"][0]
        else:
            if sim_parameters["deployment_code"] == 0:
                deploy_0(sim_parameters, Populations, pop_name, World)      
            elif sim_parameters["deployment_code"] == 1:
                deploy_1(sim_parameters, Populations, pop_name, World)  
            elif sim_parameters["deployment_code"] == 2:
                deploy_2(sim_parameters, Populations, pop_name, World)  
            elif sim_parameters["deployment_code"] == 3:
                deploy_3(sim_parameters, Populations, pop_name, World)  
            elif sim_parameters["deployment_code"] == 4:
                deploy_4(sim_parameters, Populations, pop_name, World)    
            max = sim_parameters["maximum_generations"]
            generation_count = 0
        write_parameters(sim_parameters, pop_name)
        Populations[pop_name].generation = generation_count
    while generation_count < max:
        generation_count = generation_count + 1
        for pop_name in Populations:
            sim_functions.ecoregulate(World)
            eco_cell_iterator(World, sim_parameters, 
                              sim_functions.update_ecology)
            eco_cell_iterator(World, sim_parameters, 
                              sim_functions.update_local)
            if sim_parameters["interpret_chromosome"]:
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
                (con, cur) = db_report(con, cur, sim_functions, 
                                       sim_parameters["starting_time"],
                                       Populations, World, generation_count)
    for pop_name in Populations: close_results(sim_parameters, pop_name)
    if sim_parameters.has_key("database_file") and \
        sim_parameters.has_key("database_logging_frequency"): 
        con.commit()
        con.close()
    copyfile(inspect.stack()[2][1], sim_parameters['directory'] + inspect.stack()[2][1])

def coordinates(location):
    x = location[0]
    y = location[1]
    z = location[2]
    return (x,y,z)

def adjacent_cells(sim_parameters, location):
    trashbin = []
    temp_cells = []
    world_size = [sim_parameters["world_x"],
                  sim_parameters["world_y"],
                  sim_parameters["world_z"]]
    for i in xrange(3):
        new_location = [spot for spot in location]
        new_location[0] += 1
        temp_cells.append(new_location)
        new_location = [spot for spot in location]
        new_location[0] -= 1
        temp_cells.append(new_location)    
    for i in xrange(2):
        new_location = [spot for spot in location]
        new_location[1] -= 1
        temp_cells.append(new_location) 
    for i in xrange(0,4,3):
        temp_cells[i][1] += 1
        temp_cells[i+1][1] -= 1
    temp_cells[-1][1] += 2
    for i in xrange(8):
        for x in xrange(2):
            if temp_cells[i][x] >= world_size[x] or temp_cells[i][x] < 0:
                if temp_cells[i] not in trashbin:
                    trashbin.append(temp_cells[i])
    for location in trashbin:
        temp_cells.remove(location)
    return [tuple(location) for location in temp_cells]

def spawn_populations(sim_parameters):
    temp_Populations = {}
    for pop_name in sim_parameters["population_names"]:
        temp_Populations[pop_name] = genetic.population_constructor(sim_parameters)
        for individual in temp_Populations[pop_name].agents:
            individual.generate_name()
            individual.status['deme'] = pop_name
    return temp_Populations

def eco_cell_iterator(World, sim_parameters, function):
    for x in range(sim_parameters["world_x"]):
        for y in range(sim_parameters["world_y"]):
            for z in range(sim_parameters["world_z"]):
                if len(inspect.getargspec(function)[0]) == 5:
                    function(World, x, y, z)
                else:
                    function(World)

def deploy_0(sim_parameters, Populations, pop_name, World):
    sim_parameters["deployment_scheme"](Populations, pop_name, World)

def deploy_1(sim_parameters, Populations, pop_name, World):
    position = sim_parameters["population_names"].index(pop_name)
    locations = [location for location in sim_parameters["population_locations"][position]]
    (x,y,z) = coordinates(locations[0])
    World.ecosystem[x][y][z]['organisms'] = sim_parameters["population_size"]
    for individual in Populations[pop_name].agents:
        individual.status['location'] = locations[0]

def deploy_2(sim_parameters, Populations, pop_name, World):
    position = sim_parameters["population_names"].index(pop_name)
    locations = [location for location in sim_parameters["population_locations"][position]]
    for individual in Populations[pop_name].agents:
            location = random.choice(locations)
            (x,y,z) = coordinates(location)
            while World.ecosystem[x][y][z]['organisms'] >= sim_parameters["eco_cell_capacity"]:
                location = random.choice(locations)
                (x,y,z) = coordinates(location)
            World.ecosystem[x][y][z]['organisms'] = World.ecosystem[x][y][z]['organisms'] + 1
            individual.status['location'] = location

def deploy_3(sim_parameters, Populations, pop_name, World):
    position = sim_parameters["population_names"].index(pop_name)
    locations = [location for location in sim_parameters["population_locations"][position]]
    iterator = 0
    for i in xrange(sim_parameters["population_size"]):
        individual = Populations[pop_name].agents[i]
        location = locations[iterator]
        (x,y,z) = coordinates(location)
        World.ecosystem[x][y][z]['organisms'] = World.ecosystem[x][y][z]['organisms'] + 1
        individual.status['location'] = location
        iterator += 1
        if iterator == len(locations):
            iterator = 0

def deploy_4(sim_parameters, Populations, pop_name, World):
    position = sim_parameters["population_names"].index(pop_name)
    locations = [location for location in sim_parameters["population_locations"][position]]
    adj_cells = adjacent_cells(sim_parameters, locations[0])
    for group in xrange((sim_parameters["population_size"]/sim_parameters["eco_cell_capacity"]) + 1):
        start = sim_parameters["eco_cell_capacity"] * group
        end = start + sim_parameters["eco_cell_capacity"]
        for x in xrange(start,end):
            if x == sim_parameters["population_size"]: break
            individual = Populations[pop_name].agents[x]
            if x > (sim_parameters["eco_cell_capacity"] - 1):
                location = random.choice(adj_cells)
                (x,y,z) = coordinates(location)
                while World.ecosystem[x][y][z]['organisms'] > sim_parameters["eco_cell_capacity"]:
                    location = random.choice(adj_cells)
                    (x,y,z) = coordinates(random.choice(adj_cells))
            (x,y,z) = coordinates(location)
            World.ecosystem[x][y][z]['organisms'] += 1
            individual.status['location'] = location

def interpret_chromosome(sim_parameters, Populations, pop_name, World):
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
            array = Populations[pop_name].agents[i].status['blood']
            try: (array, apointer, inputdata, output, source, spointer) = \
                register_machine.interpret(source, ragaraja.ragaraja, 3,
                                           inputdata, array,
                                           sim_parameters["max_tape_length"], 
									       sim_parameters["max_codon"])
            except Exception, e: 
                error_msg = '|'.join(['Error at Chromosome_' + \
                    str(chromosome_count), str(e)])
                Populations[pop_name].agents[i].status['chromosome_error'] = error_msg
                Populations[pop_name].agents[i].status['blood'] = array
            Populations[pop_name].agents[i].status['blood'] = array
            World.ecosystem[x][y][z]['temporary_input'] = inputdata
            World.ecosystem[x][y][z]['temporary_output'] = output

def step(Populations, pop_name, sim_functions):
    if Populations[pop_name].generation > 0:
        sim_functions.prepopulation_control(Populations, pop_name)
    sim_functions.mating(Populations, pop_name)
    sim_functions.postpopulation_control(Populations, pop_name)
    for organism in Populations[pop_name].agents:
        sim_functions.mutation_scheme(organism)
    sim_functions.generation_events(Populations, pop_name)
    Populations[pop_name].generation = Populations[pop_name].generation + 1
    return sim_functions.population_report(Populations, pop_name)

def report_generation(sim_parameters, Populations, pop_name, sim_functions, generation_count):
    report = step(Populations, pop_name, sim_functions)
    if generation_count % int(sim_parameters["fossilized_frequency"]) == 0:
        file = '%s%s_%s_' % (sim_parameters["directory"],
                             sim_parameters["simulation_name"], pop_name)
        freeze_population(file, sim_parameters["fossilized_ratio"], Populations, pop_name)
    if generation_count % int(sim_parameters["print_frequency"]) == 0:
        print '\nGENERATION: %s \n%s' % (str(generation_count), str(report))
        f = open(('%s%s_%s.result.txt' % (sim_parameters["directory"],
                                          sim_parameters["simulation_name"], 
                                          pop_name)), 'a')
        dtstamp = str(datetime.utcnow())
        f.write('\n'.join(['\n' + dtstamp, 'GENERATION: ' + str(generation_count), str(report)]))
        f.write('\n')
        f.close

def bury_world(sim_parameters, World, generation_count):
    if generation_count % int (sim_parameters["eco_buried_frequency"]) == 0:
       filename = '%s%s_gen%s.eco' % (sim_parameters["directory"], 
                                      sim_parameters["simulation_name"], 
                                      str(generation_count))
       f = open(filename, 'w')
       cPickle.dump(World, f)
       f.close()

def excavate_world(eco_file):
    f = open(eco_file, 'r')
    return cPickle.load(f)

def freeze_population(file, proportion, Populations, pop_name):
    if proportion > 1.0: proportion = 1.0
    agents = Populations[pop_name].agents
    if len(agents) < 101 or len(agents) * proportion < 101:
        sample = deepcopy(Populations[pop_name])
    else:
        new_agents = [agents[random.randint(0, len(agents) - 1)]
                      for x in xrange(int(len(agents) * proportion))]
        sample = deepcopy(Populations[pop_name])
        sample.agents = new_agents
    name = ''.join([file, 'pop', str(Populations[pop_name].generation), '_',
                    str(len(sample.agents)), '.gap'])
    f = open(name, 'w')
    cPickle.dump(sample, f)
    f.close()

def revive_population(gap_file):
    f = open(gap_file, 'r')
    return cPickle.load(f)

def write_parameters(sim_parameters, pop_name):
    f = open(('%s%s_%s.result.txt' % (sim_parameters["directory"],
                                      sim_parameters["simulation_name"],
                                      pop_name)), 'a')
    f.write("""SIMULATION: %s

----------------------------------------------------------------------
""" % sim_parameters["simulation_name"])
    if ('database_source' in sim_parameters) or \
        ('sim_folder' in sim_parameters):
        f.write("SIMULATION REVIVAL STARTED: %s\n\n" % sim_parameters["starting_time"])
    else:
        f.write("SIMULATION STARTED: %s\n\n" % sim_parameters["starting_time"])
    for key in sim_parameters:
        if key not in ('deployment_scheme', 'directory', 'sim_folder'):
            f.write("%s : %s\n" % (key, sim_parameters[key]))
    f.write("""\n\nREPORT
----------------------------------------------------------------------
""")

def close_results(sim_parameters, pop_name):
    f = open(('%s%s_%s.result.txt' % (sim_parameters["directory"],
                                      sim_parameters["simulation_name"], 
                                      pop_name)), 'a')
    f.write('''
----------------------------------------------------------------------
SIMULATION ENDED: ''' + str(datetime.utcnow()))
    f.close()
