"""!
DOSSIER - Functions to Analyze Simulation Results Database and 
Periodic Archives from DOSE (Digital Organism Simulation Environment) 
Simulations. 

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
        self.record_results = True
        self.operation_count = 0
        self.sql_statements = {}
        self.last_sql_statement = ""

    def _execute_sql(self, sqlstmt, operation_type="USER"):
        """!
        Private method to execute a SQL statement recognized by SQLite.

        @param sqlstmt: SQLite SQL statement to execute.
        @type sqlstmt: String
        @param operation_type: Define type of operation. Default = "USER".
        @type operation_type: String
        @return: Pandas dataframe containing results.
        """
        dataframe = pd.read_sql_query(sqlstmt, self.con)
        statement = operation_type.upper() + "|" + sqlstmt
        self.sql_statements[self.operation_count + 1] = statement
        self.last_sql_statement = self.sql_statements[self.operation_count + 1]
        self.operation_count = self.operation_count + 1
        return dataframe

    def list_simulations(self):
        """!
        Method to list available simulation results. Logged operation 
        type = LSIM.

        Returned Pandas dataframe columns:
            - start_time (start time of simulation, which is used as 
            primary key to extract data and results pertaining to the 
            simulation)
            - simulation_name (name of simulation)

        @return: Pandas dataframe containing results.
        """
        sqlstmt = "SELECT distinct start_time, simulation_name from parameters"
        dataframe = self._execute_sql(sqlstmt, "LSIM")
        return dataframe

    def list_parameter_types(self, table, to_list=True):
        """!
        Method to list parameters types for a table. Logged operation 
        type = LPT.

        @param table: Data table to list. Allowable types are 
        "parameters", "organisms", "world", and "miscellaneous".
        @type table: String
        @param to_list: If True, returns parameter types as a list. 
        Default = True. 
        @return: if to_list == True, returns a list of results; else, 
        return Pandas dataframe containing results.
        """
        sqlstmt = "SELECT distinct key from %s" % table.lower()
        dataframe = self._execute_sql(sqlstmt, "LPT")
        if to_list:
            return [x[0] for x in dataframe.values.tolist()]
        else:
            return dataframe

    def simulation_parameters(self, start_time):
        """!
        Method to list parameters of a given simulation (by start_time).
        Logged operation type = SP1.

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
        dataframe = self._execute_sql(sqlstmt, "SP1")
        return dataframe
