'''
File containing support functions for database logging of simulations.

Date created: 10th October 2013
'''
import os
import sqlite3 as s

def prepare_database(sim_parameters):
    '''
    Connects to logging database and prepares database for use, if
    database does not exist. If the database is not present, it will 
    create the database file and create the required database tables.
    
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
        create table if not exists timechart
            (start_time text, current_time text)''')
    con.commit()
    return (con, cur)

def db_log_simulation_parameters(con, cur, sim_parameters):
    con.commit()
    return (con, cur)

def db_report(con, cur, sim_functions, 
              Populations, World, generation_count):
    sim_functions.database_report(con, cur, 
                                  Populations, World, 
                                  generation_count)
    con.commit()
    return (con, cur)

    