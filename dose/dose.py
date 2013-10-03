import sys, os, random
from datetime import datetime

import ragaraja, register_machine
import dose_world, genetic

class simulation_functions(dose_world.World):
    pass

def spawn_populations(sim_param):
    temp_Populations = {}
    for pop_name in sim_param["population_names"]:
        temp_Populations[pop_name] = genetic.population_constructor(sim_param)
        for individual in temp_Populations[pop_name].agents:
            individual.generate_name()
            individual.status['deme'] = pop_name
    return temp_Populations

def eco_cell_locator(sim_param, function):
    for x in range(sim_param["world_x"]):
        for y in range(sim_param["world_y"]):
            for z in range(sim_param["world_z"]):
                function(x,y,z)

def eco_cell_executor(sim_param, function):
    for x in range(sim_param["world_x"]):
        for y in range(sim_param["world_y"]):
            for z in range(sim_param["world_z"]):
                function()

def coordinates(location):
    x = location[0]
    y = location[1]
    z = location[2]
    return (x,y,z)

def adjacent_cells(sim_param, location):
    trashbin = []
    temp_cells = []
    world_size = [sim_param["world_x"],sim_param["world_y"],sim_param["world_z"]]
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
    
def deploy(sim_param, Populations, World, pop_name):
   
    locations = [location for location in sim_param["population_locations"][sim_param["population_names"].index(pop_name)]]
    if sim_param["deployment_code"] == 1:
        location = locations[0]
        (x,y,z) = coordinates(location)
        World.ecosystem[x][y][z]['organisms'] = sim_param["population_size"]
        for individual in Populations[pop_name].agents:
            individual.status['location'] = location
    elif sim_param["deployment_code"] == 2:
        for individual in Populations[pop_name].agents:
            location = random.choice(locations)
            (x,y,z) = coordinates(location)
            while World.ecosystem[x][y][z]['organisms'] >= sim_param["eco_cell_capacity"]:
                location = random.choice(locations)
                (x,y,z) = coordinates(location)
            World.ecosystem[x][y][z]['organisms'] += 1
            individual.status['location'] = location
    elif sim_param["deployment_code"] == 3:
        iterator = 0
        for i in xrange(sim_param["population_size"]):
            individual = Populations[pop_name].agents[i]
            location = locations[iterator]
            (x,y,z) = coordinates(location)
            World.ecosystem[x][y][z]['organisms'] += 1
            individual.status['location'] = location
            iterator += 1
            if iterator == len(locations):
                iterator = 0
    elif sim_param["deployment_code"] == 4:
        location = locations[0]
        adj_cells = adjacent_cells(sim_param, location)
        for group in xrange((sim_param["population_size"]/sim_param["eco_cell_capacity"]) + 1):
            start = sim_param["eco_cell_capacity"] * group
            end = start + sim_param["eco_cell_capacity"]
            for x in xrange(start,end):
                if x == sim_param["population_size"]: break
                individual = Populations[pop_name].agents[x]
                if x > (sim_param["eco_cell_capacity"] - 1):
                    location = random.choice(adj_cells)
                    (x,y,z) = coordinates(location)
                    while World.ecosystem[x][y][z]['organisms'] > sim_param["eco_cell_capacity"]:
                        location = random.choice(adj_cells)
                        (x,y,z) = coordinates(location)
                (x,y,z) = coordinates(location)
                World.ecosystem[x][y][z]['organisms'] += 1
                individual.status['location'] = location

def interpret_chromosome(sim_param, Populations, World, pop_name):
    cell = [0] * sim_param["cells"]
    for individual in Populations[pop_name].agents:
        location = individual.status['location']
        (x,y,z) = coordinates(location)
        inputdata = World.ecosystem[x][y][z]['local_input']
        output = World.ecosystem[x][y][z]['local_output']
        source = ''.join(individual.genome[0].sequence)
        if sim_param["clean_cell"]:
            array = [0] * sim_param["cells"]
        else:
            array = individual.World.cell
        try: (array, apointer, inputdata, output, source, spointer) = \
            register_machine.interpret(source, ragaraja.ragaraja, 3,
                                       inputdata, array,
                                       sim_param["max_cell_population"], 
									   sim_param["max_codon"])
        except Exception: pass
        individual.cell = array
        World.ecosystem[x][y][z]['temporary_input'] = inputdata
        World.ecosystem[x][y][z]['temporary_output'] = output

def step(Populations, pop_name, Entities):
    if Populations[pop_name].generation > 0:
        Entities.prepopulation_control()
    Entities.mating()
    Entities.postpopulation_control()
    for organism in Populations[pop_name].agents:
        Entities.mutation_scheme(organism)
    Entities.generation_events()
    Populations[pop_name].generation += 1
    return Entities.population_report(Populations, pop_name)

def report_generation(sim_param, Populations, pop_name, Entities, generation_count):
    report = step(Populations, pop_name, Entities)
    if generation_count % int(sim_param["fossilized_frequency"]) == 0:
        file = '%s%s_%s_' % (sim_param["directory"],
                             sim_param["simulation_code"], pop_name)
        Populations[pop_name].freeze(file, sim_param["fossilized_ratio"])
    if generation_count % int(sim_param["print_frequency"]) == 0:
        print '\nGENERATION: %s \n%s' % (str(generation_count), str(report))
        f = open(('%s%s_%s.result.txt' % (sim_param["directory"],
                                          sim_param["simulation_code"], 
                                          pop_name)), 'a')
        dtstamp = str(datetime.utcnow())
        f.write('\n'.join(['\n' + dtstamp, 'GENERATION: ' + str(generation_count), str(report)]))
        f.write('\n')
        f.close

def bury_world(sim_param, generation_count, World):
    if generation_count % int (sim_param["eco_buried_frequency"]) == 0:
       filename = '%s%s_gen%s.eco' % (sim_param["directory"], 
                                      sim_param["simulation_code"], 
                                      str(generation_count))
       World.eco_burial(filename)

def write_parameters(sim_param, pop_name):
    f = open(('%s%s_%s.result.txt' % (sim_param["directory"],
                                      sim_param["simulation_code"], 
                                      pop_name)), 'a')
    f.write('''SIMULATION CODE: %(simulation_code)s                     %(starting_time)s
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
''' % (sim_param))
	
    f.close()

def simulate(parameters, dose_functions):
    
    Entities = dose_functions()
    time = str(datetime.utcnow())
    directory = "%s\\Simulations\\%s_%s\\" % (os.getcwd(), parameters["simulation_code"], time[0:10])
    if not os.path.exists(directory):
        os.makedirs(directory)
    parameters.update({"initial_chromosome":['0'] * parameters["chromosome_size"],
					   "fitness_function": Entities.fitness,
					   "mutation_scheme": Entities.mutation_scheme,
					   "prepopulation_control": Entities.prepopulation_control,
					   "postpopulation_control": Entities.postpopulation_control,
					   "mating": Entities.mating,
					   "generation_events": Entities.generation_events,
					   "population_report": Entities.population_report,
					   "starting_time": time, 
					   "directory": directory})
    Populations = spawn_populations(parameters)
    ragaraja.activate_version(parameters["ragaraja_version"])
    for pop_name in Populations:
        write_parameters(parameters, pop_name)
        deploy(parameters, Populations, Entities, pop_name)          
        generation_count = 0
        while generation_count < parameters["maximum_generations"]:
            generation_count += 1
            Entities.ecoregulate()
            eco_cell_locator(parameters, Entities.update_ecology)
            eco_cell_locator(parameters, Entities.update_local)
            interpret_chromosome(parameters, Populations, Entities, pop_name)
            report_generation(parameters, Populations, pop_name, Entities, generation_count)
            eco_cell_locator(parameters, Entities.organism_movement)
            eco_cell_locator(parameters, Entities.organism_location)
            eco_cell_executor(parameters, Entities.report)
            bury_world(parameters, generation_count, Entities)