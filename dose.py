import sys, os, random
from datetime import datetime

import ragaraja, register_machine
import dose_world, genetic

class dose_entities(dose_world.World):
    pass

def spawn_populations(p):
    temp_pop = {}
    for population in p["population_names"]:
        temp_pop[population] = genetic.population_constructor(p)
    return temp_pop

def eco_cell_locator(p, function):
    for x in range(p["world_x"]):
        for y in range(p["world_y"]):
            for z in range(p["world_z"]):
                function(x,y,z)

def eco_cell_executor(p, function):
    for x in range(p["world_x"]):
        for y in range(p["world_y"]):
            for z in range(p["world_z"]):
                function()

def coordinates(location):
    x = location[0]
    y = location[1]
    z = location[2]
    return (x,y,z)

def deploy(p, Populations, Entities, population):
    location = p["population_locations"][p["population_names"].index(population)]
    (x,y,z) = coordinates(location)
    Entities.ecosystem[x][y][z]['organisms'] = p["population_size"]
    for individual in Populations[population].agents:
        individual.status['location'] = location

def interpret_chromosome(p, Populations, Entities, population):
    for individual in Populations[population].agents:
        location = individual.status['location']
        (x,y,z) = coordinates(location)
        inputdata = Entities.ecosystem[x][y][z]['local_input']
        output = Entities.ecosystem[x][y][z]['local_output']
        source = ''.join(individual.genome[0].sequence)

        if p["clean_cell"]:
            array = [0] * p["cells"]
        else:
            array = individual.Entities.cell
        
        try: (array, apointer, inputdata, output, source, spointer) = \
            register_machine.interpret(source, ragaraja.ragaraja, 3,
                                       inputdata, array,
                                       p["max_cell_population"], p["max_codon"])
        except Exception: pass
            
        individual.cell = array
        Entities.ecosystem[x][y][z]['temporary_input'] = inputdata
        Entities.ecosystem[x][y][z]['temporary_output'] = output

def step(Populations, population, Entities):
    if Populations[population].generation > 0:
        Entities.prepopulation_control()
    Entities.mating()
    Entities.postpopulation_control()
    for organism in Populations[population].agents:
        Entities.mutation_scheme(organism)
    Entities.generation_events()
    Populations[population].generation += 1
    return Entities.population_report(Populations[population])

def report_generation(p, Populations, population, Entities, generation_count):
    report = step(Populations, population, Entities)
    if generation_count % int(p["fossilized_frequency"]) == 0:
        file = '%s%s_%s_' % (p["directory"],
                             p["simulation_code"], population)
        Populations[population].freeze(file, p["fossilized_ratio"])
    if generation_count % int(p["print_frequency"]) == 0:
        print '\nGENERATION: %s \n%s' % (str(generation_count), str(report))
        f = open(('%s%s_%s.result.txt' % (p["directory"],
                                          p["simulation_code"], 
                                          population)), 'a')
        dtstamp = str(datetime.utcnow())
        f.write('\n'.join(['\n' + dtstamp, 'GENERATION: ' + str(generation_count), str(report)]))
        f.write('\n')
        f.close

def bury_world(p, generation_count, Entities):
    if generation_count % int (p["eco_buried_frequency"]) == 0:
       filename = '%s%s_gen%s.eco' % (p["directory"], 
                                      p["simulation_code"], 
                                      str(generation_count))
       Entities.eco_burial(filename)

def write_parameters(p, population):
    f = open(('%s%s_%s.result.txt' % (p["directory"],
                                      p["simulation_code"], 
                                      population)), 'a')
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
''' % p)
    f.close()

def simulate(parameters, entities):
    
    Entities = entities()
    
    time = str(datetime.utcnow())
    directory = "%s\\Simulations\\%s_%s\\" % (os.getcwd(), parameters["simulation_code"], time[0:10])
    
    if not os.path.exists(directory):
        os.makedirs(directory)

    parameters.update({"initial_chromosome":['0'] * parameters["chromosome_size"],
          "mutation_scheme": Entities.mutation_scheme,
          "fitness_function": Entities.fitness,
          "prepopulation_control": Entities.prepopulation_control,
          "mating": Entities.mating,
          "postpopulation_control": Entities.postpopulation_control,
          "generation_events": Entities.generation_events,
          "population_report": Entities.population_report,
          "starting_time": time,
          "directory": directory})

    Populations = spawn_populations(parameters)

    ragaraja.activate_version(parameters["ragaraja_version"])

    for population in Populations:
        write_parameters(parameters, population)
        deploy(parameters, Populations, Entities, population)
    
        generation_count = 0
        while generation_count < parameters["maximum_generations"]:
            generation_count += 1
            Entities.ecoregulate()
            
            eco_cell_locator(parameters, Entities.update_ecology)
            eco_cell_locator(parameters, Entities.update_local)

            interpret_chromosome(parameters, Populations, Entities, population)

            report_generation(parameters, Populations, population, Entities, generation_count)

            eco_cell_locator(parameters, Entities.organism_movement)
            eco_cell_locator(parameters, Entities.organism_location)

            eco_cell_executor(parameters, Entities.report)

            bury_world(parameters, generation_count, Entities)
