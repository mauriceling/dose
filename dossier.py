"""!
DOSSIER - A Library of Utility Functions to Analyze Simulation Results 
Database from DOSE (Digital Organism Simulation Environment) Simulations. 

Date created: 17th April 2021
"""

import os
import sqlite3 as s
import sys

import pandas as pd

def connect_db(path):
    """!
    Function to connect to a DOSE simulation results database.

    @param path: Absolute or relative path to DOSE simulation results 
    database.
    @type path: String
    @return: Object representing a DOSE simulation results database.
    """
    database_object = DOSE_Result_Database(path)
    print("Connect to DOSE Results Database ...")
    print("(Relative) Path = %s" % database_object.path)
    print("Absolute Path = %s" % database_object.abspath)
    return database_object

class DOSE_Result_Database(object):
    """!
    Class to encapsulate a DOSE simulation results database. The data 
    tables in a DOSE simulation results database are:
        - parameters (start_time text, simulation_name text, key text, 
        value text)
        - organisms (start_time text, pop_name text, org_name text, 
        generation text, key text, value text)
        - world (start_time text, x text, y text, z text, generation 
        text, key text, value text)
        - miscellaneous (start_time text, generation text, key text, 
        value text)
    """
    def __init__(self, path):
        """!
        Initialization method.

        @param path: Absolute or relative path to DOSE simulation results 
        database.
        @type path: String
        """
        self.path = path
        self.abspath = os.path.abspath(self.path)
        self.con = s.connect(self.abspath)
        self.sql_statements = []

    def execute_sql(self, sqlstmt):
        """!
        Method to execute a user-defined SQL statement recognized by 
        SQLite.

        @param sqlstmt: SQLite SQL statement to execute.
        @type sqlstmt: String
        @return: Pandas dataframe containing results.
        """
        dataframe = pd.read_sql_query(sqlstmt, self.con)
        self.sql_statements.append(sqlstmt)
        return dataframe

    def list_simulations(self):
        """!
        Method to list available simulation results.

        Returned Pandas dataframe columns:
            - start_time (start time of simulation, which is used as 
            primary key to extract data and results pertaining to the 
            simulation)
            - simulation_name (name of simulation)

        @param sqlstmt: SQLite SQL statement to execute.
        @type sqlstmt: String
        @return: Pandas dataframe containing results.
        """
        sqlstmt = "SELECT distinct start_time, simulation_name from parameters"
        dataframe = pd.read_sql_query(sqlstmt, self.con)
        self.sql_statements.append(sqlstmt)
        return dataframe

    def list_simulation_parameters(self, start_time):
        """!
        Method to list parameters of a given simulation (by start_time).

        Returned Pandas dataframe columns:
            - key (parameter name)
            - value (parameter value)

        @param start_time: Start time of simulation, which is used as 
        primary key to extract data and results pertaining to the 
        simulation
        @type start_time: String
        @return: Pandas dataframe containing results.
        """
        sqlstmt = "SELECT distinct key, value from parameters where start_time = '%s' and key != 'interpreter' and key != 'deployment_scheme'" % str(start_time)
        dataframe = pd.read_sql_query(sqlstmt, self.con)
        self.sql_statements.append(sqlstmt)
        return dataframe
