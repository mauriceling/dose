'''
File containing support functions for database logging of simulations.

Date created: 10th October 2013
'''
import os
import sqlite3 as s

def prepare_database(sim_parameters):
    '''
    Connects to logging database and prepares database for use, if
    database does not exist. This function will look for database file in
    <simulation execution directory>/Simulations/<database file>. If the 
    database is not present, it will create a SQLite3 database file and 
    create the required database tables.
    
    @param filepath: File path for logging database.
    @type filepath: string
    @return: (con, cur) where con = connector and cur = cursor. 
    '''
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
    1. Population name (key = "population_names") is a list of names. 
    These are concatenated and delimited by '|'. For example, 
    ['pop_01', 'pop_02'] ==> pop_01|pop_02
    2. Genetic bases (key = "chromosome_bases") is a list of bases to make 
    up the genetic code. These are concatenated and delimited by '|'. For 
    example, ['1', '2'] ==> 1|2
    3. Ragaraja instructions to be used (key = "ragaraja_instructions") is 
    a list of 3-character Ragaraja instructions in numbers. These are 
    concatenated and delimited by '|'. For example, ['000', '004', '008'] 
    ==> 000|004|008
    4. Initial (ancestral) chromosome is a list of bases. These bases 
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
    @param Population: A dictionary containing one or more populations 
    where the value is a genetic.Population object.
    @param World: dose_world.World object.
    @return: (con, cur) where con = connector and cur = cursor. 
    '''
    sim_functions.database_report(con, cur, start_time,
                                  Populations, World, generation_count)
    con.commit()
    return (con, cur)

    