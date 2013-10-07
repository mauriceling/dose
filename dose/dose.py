import sys, os, random, inspect
from datetime import datetime

import ragaraja, register_machine
import dose_world, genetic

class world_builder(dose_world.World):
    def __init__(self, world_x, world_y, world_z):
        super(world_builder, self).__init__(world_x, world_y, world_z)

def spawn_populations(sim_parameters):
    temp_Populations = {}
    for pop_name in sim_parameters["population_names"]:
        temp_Populations[pop_name] = genetic.population_constructor(sim_parameters)
        for individual in temp_Populations[pop_name].agents:
            individual.generate_name()
            individual.status['deme'] = pop_name
    return temp_Populations

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

def eco_cell_iterator(World, sim_parameters, function):
    for x in range(sim_parameters["world_x"]):
        for y in range(sim_parameters["world_y"]):
            for z in range(sim_parameters["world_z"]):
                if len(inspect.getargspec(function)[0]) == 5:
                    function(World, x, y, z)
                else:
                    function()

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
    
def deploy(sim_parameters, Populations, pop_name, World):
    position = sim_parameters["population_names"].index(pop_name)
    locations = [location for location in sim_parameters["population_locations"][position]]
    if sim_parameters["deployment_code"] == 0:
        sim_parameters["deployment_scheme"](Populations, pop_name, World)
    if sim_parameters["deployment_code"] == 1:
        location = locations[0]
        (x,y,z) = coordinates(location)
        World.ecosystem[x][y][z]['organisms'] = sim_parameters["population_size"]
        for individual in Populations[pop_name].agents:
            individual.status['location'] = location
    elif sim_parameters["deployment_code"] == 2:
        for individual in Populations[pop_name].agents:
            location = random.choice(locations)
            (x,y,z) = coordinates(location)
            while World.ecosystem[x][y][z]['organisms'] >= sim_parameters["eco_cell_capacity"]:
                location = random.choice(locations)
                (x,y,z) = coordinates(location)
            World.ecosystem[x][y][z]['organisms'] = World.ecosystem[x][y][z]['organisms'] + 1
            individual.status['location'] = location
    elif sim_parameters["deployment_code"] == 3:
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
    elif sim_parameters["deployment_code"] == 4:
        location = locations[0]
        adj_cells = adjacent_cells(sim_parameters, location)
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
                        (x,y,z) = coordinates(location)
                (x,y,z) = coordinates(location)
                World.ecosystem[x][y][z]['organisms'] += 1
                individual.status['location'] = location

def interpret_chromosome(sim_parameters, Populations, pop_name, World):
    cell = [0] * sim_parameters["cells"]
    for individual in Populations[pop_name].agents:
        location = individual.status['location']
        (x,y,z) = coordinates(location)
        inputdata = World.ecosystem[x][y][z]['local_input']
        output = World.ecosystem[x][y][z]['local_output']
        source = ''.join(individual.genome[0].sequence)
        if sim_parameters["clean_cell"]:
            array = [0] * sim_parameters["cells"]
        else:
            array = individual.cell
        try: (array, apointer, inputdata, output, source, spointer) = \
            register_machine.interpret(source, ragaraja.ragaraja, 3,
                                       inputdata, array,
                                       sim_parameters["max_cell_population"], 
									   sim_parameters["max_codon"])
        except Exception: pass
        individual.cell = array
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
        Populations[pop_name].freeze(file, sim_parameters["fossilized_ratio"])
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
       World.eco_burial(filename)

def write_parameters(sim_parameters, pop_name):
    f = open(('%s%s_%s.result.txt' % (sim_parameters["directory"],
                                      sim_parameters["simulation_name"], 
                                      pop_name)), 'a')
    f.write('''SIMULATION: %(simulation_name)s                     
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
''' % (sim_parameters))
    f.close()

def simulate(sim_parameters, simulation_functions):
    sim_functions = simulation_functions()
    World = world_builder(sim_parameters["world_x"],
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
            eco_cell_iterator(World, sim_parameters, sim_functions.organism_movement)
            eco_cell_iterator(World, sim_parameters, sim_functions.organism_location)
            eco_cell_iterator(World, sim_parameters, sim_functions.report)
            bury_world(sim_parameters, World, generation_count)
        f = open(('%s%s_%s.result.txt' % (sim_parameters["directory"],
                                      sim_parameters["simulation_name"], 
