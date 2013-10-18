'''
File containing support functions for database logging of simulations.

Date created: 10th October 2013
'''
import os
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
    @return: (con, cur) where con = connector and cur = cursor. 
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
    
    @param con: Database connector from prepare_database() function. 
    @param cur: Database cursor from prepare_database() function.
    @param sim_parameters: Dictionary of parameters used in simulation.
    @return: (con, cur) where con = connector and cur = cursor. 
    '''
    start_time = sim_parameters["starting_time"]
    simulation_name = sim_parameters["simulation_name"]
    for key in [k for k in sim_parameters.keys() 
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
    
    @param con: Database connector from prepare_database() function. 
    @param cur: Database cursor from prepare_database() function.
    @param sim_functions: Object of simulation-specific functions, which 
    inherits dose.dose_functions class.
    @param start_time: Starting time of current simulation in the format 
    of <date>-<seconds since epoch>; for example, 2013-10-11-1381480985.77.
    @param Populations: A dictionary containing one or more populations 
    where the value is a genetic.Population object.
    @param World: dose_world.World object.
    @return: (con, cur) where con = connector and cur = cursor. 
    '''
    sim_functions.database_report(con, cur, start_time,
                                  Populations, World, generation_count)
    con.commit()
    return (con, cur)

def db_list_simulations(cur, table='parameters'):
    if table not in ('parameters', 'organisms',
                     'world', 'miscellaneous'):
        table = 'parameters'
    if table == 'parameters':
        cur.execute("""select distinct start_time, simulation_name 
                    from parameters""")
    else:
        cur.execute("select distinct start_time from %s", table)
    return cur.fetchall()

def db_reconstruct_simulation_parameters(cur, start_time):
    parameters = {"simulation_name": None,
                  "population_names": None,
                  "population_locations": None,
                  "deployment_code": None,
                  "chromosome_bases": None,
                  "background_mutation": None,
                  "additional_mutation": None,
                  "mutation_type": None,
                  "chromosome_size": None,
                  "genome_size": None,
                  "max_tape_length": None,
                  "clean_cell": None,
                  "interpret_chromosome": None,
                  "max_codon": None,
                  "population_size": None,
                  "eco_cell_capacity": None,
                  "world_x": None,
                  "world_y": None,
                  "world_z": None,
                  "goal": None,
                  "maximum_generations": None,
                  "fossilized_ratio": None,
                  "fossilized_frequency": None,
                  "print_frequency": None,
                  "ragaraja_version": None,
                  "ragaraja_instructions": None,
                  "eco_buried_frequency": None,
                  "database_file": None,
                  "database_logging_frequency": None}
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
            try:
                parameters['goal'] = float(r[1])
            except ValueError:
                exec("parameters['goal'] = %s" % str(r[1]))
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
            if version == '0.1':
                parameters['ragaraja_version'] = 0.1
            else:
                parameters['ragaraja_version'] = int(r[1])
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
    