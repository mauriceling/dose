'''
File containing support functions for database logging of simulations.

Date created: 10th October 2013
'''
import os, copy
import sqlite3 as s

def connect_database(dbpath, sim_parameters=None):
    '''
    Connects to logging database and prepares database for use, if
    database does not exist. This function can be used to connect to the 
    logging database using a file path or using simulation parameters 
    dictionary. 
    
    Simulation parameters dictionary takes precedence - if simulation 
    parameters dictionary (sim_parameters) is not None, this function will 
    look for database file in <simulation execution directory>/Simulations/
    <database file>. 
    
    In both cases, if the database is not present, it will create a SQLite3 
    database file and create the required database tables.
    
    @param dbpath: File path of logging database. This parameter will only 
    be used when sim_parameters == None.
    @param sim_parameters: Dictionary of simulation parameters. Default is 
    None.
    @return: (con, cur) where 
        - con = connector
        - cur = cursor
    '''
    if sim_parameters:
        dbpath = os.sep.join([os.getcwd(), 
                              'Simulations', 
                              sim_parameters["database_file"]])
    con = s.connect(dbpath)
    cur = con.cursor()
    cur.execute('''
        create table if not exists parameters
            (start_time text, simulation_name text,
             key text, value text)''')
    cur.execute('''
        create table if not exists organisms
            (start_time text, pop_name text, 
             org_name text, generation text,
             key text, value text)''')
    cur.execute('''
        create table if not exists world
            (start_time text, x text, y text, 
             z text, generation text,
             key text, value text)''')
    cur.execute('''
        create table if not exists miscellaneous
            (start_time text, generation text,
             key text, value text)''')
    cur.execute('''
        create index if not exists organisms_index1 on organisms
            (pop_name, generation)''')
    cur.execute('''
        create index if not exists organisms_index2 on organisms
            (generation, org_name)''')
    con.commit()
    return (con, cur)

def db_log_simulation_parameters(con, cur, sim_parameters):
    '''
    Function to log the simulation parameters. A database table, parameters, 
    had been defined for simulation parameters logging where the structure 
    is (start_time text, simulation_name text, key text, value text). The 
    starting time of current simulation (start_time) and name of the 
    current simulation (simulation_name) are used as complex primary key 
    to identify the current simulation. All parameters will be logged, 
    except for "starting_time" and "simulation_name".
    
    The following transformations of data are made:
        - Population name (key = "population_names") is a list of names. 
        These are concatenated and delimited by '|'. For example, 
        ['pop_01', 'pop_02'] ==> pop_01|pop_02
        - Genetic bases (key = "chromosome_bases") is a list of bases to 
        make up the genetic code. These are concatenated and delimited by 
        '|'. For example, ['1', '2'] ==> 1|2
        - Ragaraja instructions to be used (key = "ragaraja_instructions") 
        is a list of 3-character Ragaraja instructions in numbers. These 
        are concatenated and delimited by '|'. For example, ['000', '004', 
        '008']  ==> 000|004|008
        - Initial (ancestral) chromosome is a list of bases. These bases 
        are concatenated with no delimiter. For example, [1, 2, 3] ==> 123
    
    @param con: Database connector from connect_database() function. 
    @param cur: Database cursor from connect_database() function.
    @param sim_parameters: Dictionary of parameters used in simulation.
    @return: (con, cur) where 
        - con = connector
        - cur = cursor
    '''
    start_time = sim_parameters["starting_time"]
    simulation_name = sim_parameters["simulation_name"]
    for key in [k for k in list(sim_parameters.keys()) 
                if k not in ("simulation_name", "starting_time")]:
		value = sim_parameters[key]
		if key in ("population_names", "chromosome_bases", 
                   "ragaraja_instructions"):
			value = '|'.join([str(x) for x in value])
			cur.execute('''insert into parameters values (?,?,?,?)''', 
						(str(start_time), str(simulation_name), 
						 str(key), value))
		elif key in ("initial_chromosome"):
			value = ''.join(value)
			cur.execute('''insert into parameters values (?,?,?,?)''', 
						(str(start_time), str(simulation_name), 
						 str(key), value))
		else:
			cur.execute('''insert into parameters values (?,?,?,?)''', 
						(str(start_time), str(simulation_name), 
						 str(key), str(value)))
    con.commit()
    return (con, cur)

def db_report(con, cur, sim_functions, start_time,
              Populations, World, generation_count):
    '''
    Wrapper around user-implemented database logging which over-rides 
    dose.dose_functions.database_report() function.
    
    @param con: Database connector from connect_database() function. 
    @param cur: Database cursor from connect_database() function.
    @param sim_functions: Object of simulation-specific functions, which 
    inherits dose.dose_functions class.
    @param start_time: Starting time of current simulation in the format 
    of <date>-<seconds since epoch>; for example, 2013-10-11-1381480985.77.
    @param Populations: A dictionary containing one or more populations 
    where the value is a genetic.Population object.
    @param World: dose_world.World object.
    @param generation_count: Current number of generations simulated.
    @return: (con, cur) where 
        - con = connector
        - cur = cursor 
    '''
    sim_functions.database_report(con, cur, start_time,
                                  Populations, World, generation_count)
    con.commit()
    return (con, cur)

def db_list_simulations(cur, table='parameters'):
    '''
    Function to list simulations, identified by starting time of the 
    simulation (and simulation name, if available), from logging database.
    
    @param cur: Database cursor from connect_database() function.
    @param table: Database table name to list simulations. Allowable values 
    are 'parameters', 'organisms', 'world', and 'miscellaneous'. Default 
    value is 'parameters'.
    @return: A list containing the results. 
        - If table = 'parameters', the returned list will be a list of list 
        (consisting of [starting time of simulation, simulation name]). 
        - If table is not 'parameters', the returned list will be a list of 
        starting time of simulation.
    '''
    if table not in ('parameters', 'organisms',
                     'world', 'miscellaneous'):
        table = 'parameters'
    if table == 'parameters':
        cur.execute("""select distinct start_time, simulation_name 
                    from parameters""")
        return [[str(x[0]), str(x[1])] for x in cur.fetchall()]
    else:
        cur.execute("select distinct start_time from %s", table)
        return [str(x[0]) for x in cur.fetchall()]
    
def db_list_generations(cur, start_time, table='organisms'):
    '''
    Function to list all logged generations within a simulation, identified 
    by starting time of the simulation.
    
    @param cur: Database cursor from connect_database() function.
    @param start_time: Starting time of current simulation in the format 
    of <date>-<seconds since epoch>; for example, 2013-10-11-1381480985.77.
    @param table: Database table name to list simulations. Allowable values 
    are 'parameters', 'organisms', 'world', and 'miscellaneous'. Default 
    value is 'organisms'.
    @return: A list containing the results (generation counts).
    '''
    # query plan: SCAN TABLE organisms USING COVERING INDEX organisms_index2
    cur.execute("select distinct generation from %s where start_time='%s'" 
                % (str(table), str(start_time)))
    generations = sorted([int(str(x[0])) for x in cur.fetchall()])
    return [str(gen) for gen in generations]

def db_list_datafields(cur, start_time, table='organisms'):
    '''
    Function to list all logged data fields (types of data logged) within 
    a simulation, identified by starting time of the simulation.
    
    @param cur: Database cursor from connect_database() function.
    @param start_time: Starting time of current simulation in the format 
    of <date>-<seconds since epoch>; for example, 2013-10-11-1381480985.77.
    @param table: Database table name to list simulations. Allowable values 
    are 'parameters', 'organisms', 'world', and 'miscellaneous'. Default 
    value is 'organisms'.
    @return: A list containing the results (types of data logged).
    '''
    cur.execute("select distinct key from %s where start_time='%s'" 
                % (str(table), str(start_time)))
    return [str(x[0]) for x in cur.fetchall()]

def db_list_population_name(cur, start_time):
    '''
    Function to list all logged populations (as population names) within a 
    simulation, identified by starting time of the simulation.
    
    @param cur: Database cursor from connect_database() function.
    @param start_time: Starting time of current simulation in the format 
    of <date>-<seconds since epoch>; for example, 2013-10-11-1381480985.77.
    @return: A list containing the results (types of data logged).
    '''
    # query plan: SCAN TABLE organisms USING COVERING INDEX organisms_index1
    cur.execute("select distinct pop_name from organisms where \
                start_time='%s'" % str(start_time))
    return [str(x[0]) for x in cur.fetchall()]

def db_get_ecosystem(cur, start_time, datafield='all', generation='all'):
    '''
    Analysis helper function to get a specific field of the ecosystem 
    (World.ecosystem) or the entire ecosystem for one or more generations 
    within a simulation (as identified by the starting time of the 
    simulation).
    
    @param cur: Database cursor from connect_database() function.
    @param start_time: Starting time of current simulation in the format 
    of <date>-<seconds since epoch>; for example, 2013-10-11-1381480985.77.
    @param datafield: The specific datafield in World.ecosystem to extract. 
    Predefined datafields for ecosystem are 'local_input', 'local_output',
    'temporary_input', 'temporary_output', and 'organisms'. Default = 'all', 
    which returns the entire World.ecosystem(s) of the generation(s). Only 
    one or all datafield(s) in World.ecosystem can be extracted at a time.
    @type datafield: string
    @param generation: Generation(s) to extract World.ecosystem. Default = 
    'all', which extracts World.ecosystems for all logged generations within 
    the specific simulation.
    @type generation: list
    @return: A dictionary of results - {<generation count>: <value>}. The 
    value is the value of the specific datafield if a specific datafield 
    is required (the data type of this value is dependent on that of the 
    data type of World.ecosystem[datafield]) or the entire ecosystem as a 
    dictionary. 
    '''
    if generation == 'all':
        generation = db_list_generations(cur, start_time, 'world')
    else:
        generation = [str(x) for x in generation]
    results = {}
    for gen in generation:
        results[gen] = {}
        ecosystem = db_reconstruct_world(cur, start_time, gen).ecosystem
        if datafield == 'all':
            results[gen] = ecosystem
        else:
            for x in list(ecosystem.keys()):
                results[gen][x] = {}
                for y in list(ecosystem[x].keys()):
                    results[gen][x][y] = {}
                    for z in list(ecosystem[x][y].keys()):
                        results[gen][x][y][z] = ecosystem[x][y][z][datafield]
    return results

def db_get_organisms_status(cur, start_time, population_name, 
                            datafield='all', generation='all'):
    '''
    Analysis helper function to get a specific field of the Organism.status 
    dictionary or the entire Organism.status dictionary for one or more 
    generations within a simulation (as identified by the starting time of 
    the simulation).
    
    @param cur: Database cursor from connect_database() function.
    @param start_time: Starting time of current simulation in the format 
    of <date>-<seconds since epoch>; for example, 2013-10-11-1381480985.77.
    @param population_name: Name of the population.
    @param datafield: The specific key in Organism.status dictionary to 
    extract. Predefined keys for Organism.status dictionary are'age', 
    'alive', 'blood', 'death', 'deme', 'fitness', 'gender', 'identity', 
    'lifespan', 'location', 'parents', 'vitality'. Default = 'all', which 
    returns the entire Organism.status dictionaries of the generation(s). 
    Only one or all datafield(s) in Organism.status dictionary can be 
    extracted at a time.
    @type datafield: string
    @param generation: Generation(s) to extract Organism.status dictionary. 
    Default = 'all', which extracts Organism.status dictionary for all 
    logged generations within the specific simulation.
    @type generation: list
    @return: A dictionary of dictionary of results - 
    {<generation count>: {<Organism identity>: <value>}}. The value is the 
    value of the specific datafield if a specific datafield is required 
    (the data type of this value is dependent on that of the data type of 
    Organism.status[datafield]) or the entire Organism.status as a dictionary. 
    '''
    if generation == 'all':
        generation = db_list_generations(cur, start_time, 'organisms')
    else:
        generation = [str(x) for x in generation]
    results = {}
    for gen in generation:
        results[gen] = {}
        agents = db_reconstruct_organisms(cur, start_time, 
                                          population_name, gen)
        for org in agents:
            identity = org.status['identity']
            if datafield == 'all':
                results[gen][identity] = org.status
            else:
                results[gen][identity] = org.status[datafield]
    return results

def db_get_organisms_genome(cur, start_time, 
                            population_name, generation='all'):
    '''
    Analysis helper function to get entire genome of organisms for one or 
    more generations within a simulation (as identified by the starting 
    time of the simulation).
    
    @param cur: Database cursor from connect_database() function.
    @param start_time: Starting time of current simulation in the format 
    of <date>-<seconds since epoch>; for example, 2013-10-11-1381480985.77.
    @param population_name: Name of the population.
    @param generation: Generation(s) to extract Organism.genome. 
    Default = 'all', which extracts Organism.genome for all logged 
    generations within the specific simulation.
    @type generation: list
    @return: A dictionary of dictionary of genome - 
    {<generation count>: {<Organism identity>: <genome as list of chromosomes>}}.
    '''
    if generation == 'all':
        generation = db_list_generations(cur, start_time, 'organisms')
    else:
        generation = [str(x) for x in generation]
    results = {}
    for gen in generation:
        results[gen] = {}
        agents = db_reconstruct_organisms(cur, start_time, 
                                          population_name, gen)
        for org in agents:
            identity = org.status['identity']
            results[gen][identity] = org.genome
    return results

def db_get_organisms_chromosome_sequences(cur, start_time, 
                                          population_name, 
                                          generation='all'):
    '''
    Analysis helper function to get chromosomal sequences of entire genome 
    of organisms for one or more generations within a simulation (as 
    identified by the starting time of the simulation).
    
    @param cur: Database cursor from connect_database() function.
    @param start_time: Starting time of current simulation in the format 
    of <date>-<seconds since epoch>; for example, 2013-10-11-1381480985.77.
    @param population_name: Name of the population.
    @param generation: Generation(s) to extract Organism.genome. 
    Default = 'all', which extracts Organism.genome for all logged 
    generations within the specific simulation.
    @type generation: list
    @return: A dictionary of dictionary of chromosomal sequences - 
    {<generation count>: {<Organism identity>: <list (all chromosomes) of 
    list (individual chromosome) of chromosomal sequence>}}.
    '''
    genome_dict = db_get_organisms_genome(cur, start_time, 
                                          population_name, generation)
    results = {}
    for gen in list(genome_dict.keys()):
        results[gen] = {}
        for identity in list(genome_dict[gen].keys()):
            results[gen][identity] = [chromosome.sequence 
                            for chromosome in genome_dict[gen][identity]]
    return results    

def db_reconstruct_simulation_parameters(cur, start_time):
    '''
    Function to reconstruct simulation parameters dictionary of a 
    simulation (as identified by the starting time of the simulation).
    
    @param cur: Database cursor from connect_database() function.
    @param start_time: Starting time of current simulation in the format 
    of <date>-<seconds since epoch>; for example, 2013-10-11-1381480985.77.
    @return: Simulation parameters dictionary containing the following keys: 
        - simulation_name
        - population_names
        - population_locations
        - deployment_code
        - chromosome_bases
        - background_mutation
        - additional_mutation
        - mutation_type
        - chromosome_size
        - genome_size
        - max_tape_length
        - clean_cell
        - interpret_chromosome
        - max_codon
        - population_size
        - eco_cell_capacity
        - world_x
        - world_y
        - world_z
        - goal
        - maximum_generations
        - fossilized_ratio
        - fossilized_frequency
        - print_frequency
        - ragaraja_version
        - ragaraja_instructions
        - eco_buried_frequency
        - database_file
        - database_logging_frequency
    '''
    parameters = {}
    for key in ('simulation_name', 'population_names', 
                'population_locations', 'deployment_code',
                'chromosome_bases', 'background_mutation',
                'additional_mutation', 'mutation_type',
                'chromosome_size', 'genome_size', 'max_tape_length',
                'clean_cell', 'interpret_chromosome', 'max_codon',
                'population_size', 'eco_cell_capacity',
                'world_x', 'world_y', 'world_z', 'goal',
                'maximum_generations', 'fossilized_ratio',
                'fossilized_frequency', 'print_frequency',
                'ragaraja_version', 'ragaraja_instructions',
                'eco_buried_frequency', 'database_file',
                'database_logging_frequency'):
        parameters[key] = None
    start_time = str(start_time)
    cur.execute("select distinct simulation_name from parameters where \
    start_time = '%s'" % start_time)
    parameters["simulation_name"] = str(cur.fetchone()[0])
    cur.execute("select key, value from parameters where \
                 start_time = '%s'" % start_time)
    for r in cur.fetchall():
        if str(r[0]) == 'population_names':
            value = str(r[1]).split('|')
            exec("parameters['population_names'] = %s" % str(value))
        elif str(r[0]) == 'population_locations':
            exec("parameters['population_locations'] = %s" % str(r[1]))
        elif str(r[0]) == 'deployment_code':
            parameters['deployment_code'] = int(r[1])
        elif str(r[0]) == 'chromosome_bases':
            value = str(r[1]).split('|')
            exec("parameters['chromosome_bases'] = %s" % str(value))
        elif str(r[0]) == 'background_mutation':
            parameters['background_mutation'] = float(r[1])
        elif str(r[0]) == 'additional_mutation':
            parameters['additional_mutation'] = float(r[1])
        elif str(r[0]) == 'mutation_type':
            parameters['mutation_type'] = str(r[1])
        elif str(r[0]) == 'chromosome_size':
            parameters['chromosome_size'] = int(r[1])
        elif str(r[0]) == 'genome_size':
            parameters['genome_size'] = int(r[1])
        elif str(r[0]) == 'max_tape_length':
            parameters['max_tape_length'] = int(r[1])
        elif str(r[0]) == 'clean_cell':
            exec("parameters['clean_cell'] = %s" % str(r[1]))
        elif str(r[0]) == 'interpret_chromosome':
            exec("parameters['interpret_chromosome'] = %s" % str(r[1]))
        elif str(r[0]) == 'max_codon':
            parameters['max_codon'] = int(r[1])
        elif str(r[0]) == 'population_size':
            parameters['population_size'] = int(r[1])
        elif str(r[0]) == 'eco_cell_capacity':
            parameters['eco_cell_capacity'] = int(r[1])
        elif str(r[0]) == 'world_x':
            parameters['world_x'] = int(r[1])
        elif str(r[0]) == 'world_y':
            parameters['world_y'] = int(r[1])
        elif str(r[0]) == 'world_z':
            parameters['world_z'] = int(r[1])
        elif str(r[0]) == 'goal':
            try: parameters['goal'] = float(r[1])
            except ValueError: exec("parameters['goal'] = %s" % str(r[1]))
        elif str(r[0]) == 'maximum_generations':
            parameters['maximum_generations'] = int(r[1])
        elif str(r[0]) == 'fossilized_ratio':
            parameters['fossilized_ratio'] = float(r[1])
        elif str(r[0]) == 'fossilized_frequency':
            parameters['fossilized_frequency'] = int(r[1])
        elif str(r[0]) == 'print_frequency':
            parameters['print_frequency'] = int(r[1])
        elif str(r[0]) == 'ragaraja_version':
            version = str(r[1])
            if version == '0.1': parameters['ragaraja_version'] = 0.1
            else: parameters['ragaraja_version'] = int(r[1])
        elif str(r[0]) == 'ragaraja_instructions':
            value = str(r[1]).split('|')
            exec("parameters['ragaraja_instructions'] = %s" % str(value))
        elif str(r[0]) == 'eco_buried_frequency':
            parameters['eco_buried_frequency'] = int(r[1])
        elif str(r[0]) == 'database_file':
            parameters['database_file'] = str(r[1])
        elif str(r[0]) == 'database_logging_frequency':
            parameters['database_logging_frequency'] = int(r[1])
    return parameters

def db_reconstruct_world(cur, start_time, generation):
    '''
    Function to reconstruct the world object of a simulation (as identified 
    by the starting time of the simulation) at a specific generation.
    
    @param cur: Database cursor from connect_database() function.
    @param start_time: Starting time of current simulation in the format 
    of <date>-<seconds since epoch>; for example, 2013-10-11-1381480985.77.
    @param generation: Current number of generations simulated.
    @return: dose_world.World object
    '''
    import dose_world
    eco_cell = {'local_input': [], 'local_output': [],
                'temporary_input': [], 'temporary_output': [],
                'organisms': 0}
    cur.execute("select max(x), max(y), max(z) from world where \
    start_time = '%s'" % start_time)
    coordinates = cur.fetchone()
    world_x = int(coordinates[0]) + 1
    world_y = int(coordinates[1]) + 1
    world_z = int(coordinates[2]) + 1
    ecosystem = {}
    for x in range(world_x):
        ecosystem[x] = {}
        for y in range(world_y):
            ecosystem[x][y] = {}
            for z in range(world_z): 
                ecosystem[x][y][z] = {}
                for key in ('local_input', 'local_output',
                            'temporary_input', 'temporary_output',
                            'organisms'):
                    ecosystem[x][y][z][key] = None
    start_time = str(start_time)
    generation = str(generation)
    # query plan: SCAN TABLE world
    cur.execute("select x, y, z, key, value from world where \
    start_time =  '%s' and generation = '%s'" % (start_time, generation))
    for r in cur.fetchall():
        x = int(r[0])
        y = int(r[1])
        z = int(r[2])
        key = str(r[3])
        value = str(r[4])
        exec("ecosystem[%i][%i][%i]['%s'] = %s" % (x, y, z, key, value))
    World = dose_world.World(1, 1, 1)
    World.ecosystem = ecosystem
    return World
    
def db_reconstruct_organisms(cur, start_time, population_name, generation):
    '''
    Function to reconstruct a list of organisms (genetic.Organism objects) 
    of a population within a simulation (as identified by the starting time 
    of the simulation) at a specific generation.
    
    @param cur: Database cursor from connect_database() function.
    @param start_time: Starting time of current simulation in the format 
    of <date>-<seconds since epoch>; for example, 2013-10-11-1381480985.77.
    @param population_name: Name of the population
    @param generation: Current number of generations simulated.
    @return: A list of Organisms (genetic.Organism objects)
    '''
    import genetic as g
    start_time = str(start_time)
    population_name = str(population_name)
    generation = str(generation)
    # query plan: SEARCH TABLE organisms USING INDEX 
    #             organisms_index2 (generation=?)
    cur.execute("select distinct org_name from organisms where \
    start_time = '%s' and pop_name = '%s' and generation = '%s'" %
    (start_time, population_name, generation))
    names = [x[0] for x in cur.fetchall()]
    agents = [0] * len(names)
    for i in range(len(names)):
        org_name = str(names[i])
        org = g.Organism()
        org.genome = []
        org.status['identity'] = org_name
        # query plan: SEARCH TABLE organisms USING INDEX 
        #             organisms_index2 (generation=? AND org_name=?)
        cur.execute("select key, value from organisms where \
        generation = '%s' and org_name = '%s' and \
        start_time = '%s' and pop_name = '%s'" %
        (generation, org_name, start_time, population_name))
        for r in cur.fetchall():
            key = str(r[0])
            value = str(r[1])
            if key == 'alive':
                exec("org.status['alive'] = %s" % str(value))
            elif key == 'vitality':
                org.status['vitality'] = float(value)
            elif key == 'parents':
                if value == '': value = '[]'
                else: value = value.split('|')
                exec("org.status['parents'] = %s" % str(value))
            elif key == 'age':
                org.status['age'] = float(value)
            elif key == 'gender':
                exec("org.status['gender'] = %s" % str(value)) 
            elif key == 'lifespan':
                org.status['lifespan'] = float(value)
            elif key == 'fitness':
                exec("f = '%s'" % str(value))
                if type(f) == type(1) or type(f) == type(1.0):
                    org.status['fitness'] = float(value)
                else:
                    exec("org.status['fitness'] = %s" % str(value))
            elif key == 'blood':
                if value == '': value = '[]'
                else: value = value.split('|')
                exec("org.status['blood'] = %s" % str(value))
            elif key == 'deme':
                org.status['deme'] = str(value)
            elif key == 'location':
                value = tuple([int(x) for x in value.split('|')])
                exec("org.status['location'] = %s" % str(value))
            elif key == 'death':
                exec("org.status['death'] = %s" % str(value))
            elif key.startswith('chromosome'):
                chr_position = key.split('_')[1]
                sequence = [str(x) for x in str(value)]
                cur.execute("select value from parameters where \
                    key='background_mutation' and start_time='%s'" % 
                    start_time)
                background_mutation = float(cur.fetchone()[0])
                cur.execute("select value from parameters where \
                    key='chromosome_bases' and start_time='%s'" % 
                    start_time)
                bases = str(cur.fetchone()[0]).split('|')
                exec("chromosome_bases = %s" % bases)
                chromosome = g.Chromosome(sequence, chromosome_bases, 
                                          background_mutation)
                org.genome.append(chromosome)
            else:
                exec("org.status['%s'] = %s" % (str(key), str(value)))
        agents[i] = org
    return agents
    
def db_reconstruct_population(cur, start_time, 
                              population_name, generation):
    '''
    Function to reconstruct a population within a simulation (as identified 
    by the starting time of the simulation) at a specific generation.
    
    @param cur: Database cursor from connect_database() function.
    @param start_time: Starting time of current simulation in the format 
    of <date>-<seconds since epoch>; for example, 2013-10-11-1381480985.77.
    @param population_name: Name of the population
    @param generation: Current number of generations simulated.
    @return: genetic.Population object
    '''
    import genetic
    agents = db_reconstruct_organisms(cur, start_time, 
                                      population_name, generation)
    cur.execute("select value from parameters where \
                key='goal' and start_time='%s'" % start_time)
    g = cur.fetchone()[0]
    try: goal = float(g)
    except ValueError: exec("goal = %s" % str(g))
    return genetic.Population(goal, 1e24, agents)
    