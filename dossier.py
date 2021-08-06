"""!
DOSSIER - Functions to Analyze Simulation Results Database and 
Periodic Archives from DOSE (Digital Organism Simulation Environment) 
Simulations. 

Date created: 17th April 2021
"""

import os
import sqlite3 as s
import sys

import networkx as nx
import pandas as pd

def ConnectDB(path):
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

    ##################################################################
    # 1. SQL Executor
    ##################################################################
    def _ExecuteSQL(self, sqlstmt, operation_type="USER"):
        """!
        Private method to execute a SQL statement recognized by SQLite.

        @param sqlstmt: SQLite SQL statement to execute.
        @type sqlstmt: String
        @param operation_type: Define type of operation. Default = "USER".
        @type operation_type: String
        @return: Pandas dataframe containing results.
        """
        dataframe = pd.read_sql_query(sqlstmt, self.con)
        statement = operation_type + "|" + sqlstmt
        self.sql_statements[self.operation_count + 1] = statement
        self.last_sql_statement = self.sql_statements[self.operation_count + 1]
        self.operation_count = self.operation_count + 1
        return dataframe
    ##################################################################
    # (End of) SQL Executor
    ##################################################################

    ##################################################################
    # 2. Primary Metadata Information Getter
    ##################################################################
    def Sims(self):
        """!
        Method to list available simulation results. Logged operation 
        type = SIMS.

        Returned Pandas dataframe columns:
            - start_time (start time of simulation, which is used as 
            primary key to extract data and results pertaining to the 
            simulation)
            - simulation_name (name of simulation)

        @return: Pandas dataframe containing results.
        """
        sqlstmt = "SELECT distinct start_time, simulation_name from parameters"
        dataframe = self._ExecuteSQL(sqlstmt, "SIMS")
        return dataframe

    def ParamTypes(self, table, to_list=True):
        """!
        Method to list parameters types for a table. Logged operation 
        type = PType.

        @param table: Data table to list. Allowable types are 
        "parameters", "organisms", "world", and "miscellaneous".
        @type table: String
        @param to_list: If True, returns parameter types as a list. 
        Default = True. 
        @return: if to_list == True, returns a list of results; else, 
        return Pandas dataframe containing results.
        """
        sqlstmt = "SELECT distinct key from %s" % table.lower()
        dataframe = self._ExecuteSQL(sqlstmt, "PType")
        if to_list:
            return dataframe['key'].values.tolist()
        else:
            return dataframe
    ##################################################################
    # (End of) Primary Metadata Information Getter
    ##################################################################

    ##################################################################
    # 3. Simulation Parameters (Table = parameters) Getter
    ##################################################################
    def SimParam_Time(self, start_time):
        """!
        Method to list parameters of a given simulation (by start_time).
        Logged operation type = SPTime.

        Returned Pandas dataframe columns:
            - start_time (start time of simulation, which is used as 
            primary key to extract data and results pertaining to the 
            simulation)
            - x (x-axis of ecological cell)
            - y (y-axis of ecological cell)
            - z (z-axis of ecological cell)
            - generation (generation count)
            - key (parameter name)
            - value (parameter value)

        @param start_time: Start time of simulation, which is used as 
        primary key to extract data and results pertaining to the 
        simulation
        @type start_time: String
        @return: Pandas dataframe containing results.
        """
        sqlstmt = "SELECT distinct key, value from parameters where start_time = '%s' and key != 'interpreter' and key != 'deployment_scheme'" % str(start_time)
        dataframe = self._ExecuteSQL(sqlstmt, "SPTime")
        dataframe["start_time"] = start_time
        dataframe["x"] = None
        dataframe["y"] = None
        dataframe["z"] = None
        dataframe["generation"] = None
        column_names = ["start_time", "x", "y", "z", 
                        "generation", "key", "value"]
        return dataframe.reindex(columns=column_names)

    def SimParam_Name(self, parameter):
        """!
        Method to list the values of parameter across simulations.
        Logged operation type = SPName.

        Returned Pandas dataframe columns:
            - start_time (start time of simulation, which is used as 
            primary key to extract data and results pertaining to the 
            simulation)
            - x (x-axis of ecological cell)
            - y (y-axis of ecological cell)
            - z (z-axis of ecological cell)
            - generation (generation count)
            - key (parameter name)
            - value (parameter value)

        @param parameter: Required parameter value.
        @type parameter: String
        @return: Pandas dataframe containing results.
        """
        sqlstmt = "SELECT start_time, value from parameters where key = '%s'" % str(parameter)
        dataframe = self._ExecuteSQL(sqlstmt, "SPName")
        dataframe["key"] = parameter
        dataframe["x"] = None
        dataframe["y"] = None
        dataframe["z"] = None
        dataframe["generation"] = None
        column_names = ["start_time", "x", "y", "z", 
                        "generation", "key", "value"]
        return dataframe.reindex(columns=column_names)

    def SimParam_TimeName(self, start_time, parameter):
        """!
        Method to get the value of one parameter in one simulation.
        Logged operation type = SPTN.

        @param start_time: Start time of simulation, which is used as 
        primary key to extract data and results pertaining to the 
        simulation
        @type start_time: String
        @param parameter: Required parameter value.
        @type parameter: String
        @return: Parameter value.
        """
        sqlstmt = "SELECT value from parameters where start_time = '%s' and key = '%s'" % (str(start_time), str(parameter))
        dataframe = self._ExecuteSQL(sqlstmt, "SPTN")
        return dataframe['value'].values.tolist()[0]
    ##################################################################
    # (End of) Simulation Parameters (Table = parameters) Getter
    ##################################################################

    ##################################################################
    # 4. World Parameters (Table = world) Getter
    ##################################################################
    def WorldParam_Time(self, start_time):
        """!
        Method to list world parameters of a given simulation (by start_time).
        Logged operation type = WPTime.

        Returned Pandas dataframe columns:
            - start_time (start time of simulation, which is used as 
            primary key to extract data and results pertaining to the 
            simulation)
            - x (x-axis of ecological cell)
            - y (y-axis of ecological cell)
            - z (z-axis of ecological cell)
            - generation (generation count)
            - key (parameter name)
            - value (parameter value)

        @param start_time: Start time of simulation, which is used as 
        primary key to extract data and results pertaining to the 
        simulation
        @type start_time: String
        @return: Pandas dataframe containing results.
        """
        sqlstmt = "SELECT distinct x, y, z, generation, key, value from world where start_time = '%s'" % str(start_time)
        dataframe = self._ExecuteSQL(sqlstmt, "WPTime")
        dataframe["start_time"] = start_time
        column_names = ["start_time", "x", "y", "z", 
                        "generation", "key", "value"]
        return dataframe.reindex(columns=column_names)

    def WorldParam_TimeCell(self, start_time, x, y, z):
        """!
        Method to list the parameters of a specific ecological cell of 
        a given simulation (by start_time). Logged operation type = 
        WPTCell.

        Returned Pandas dataframe columns:
            - start_time (start time of simulation, which is used as 
            primary key to extract data and results pertaining to the 
            simulation)
            - x (x-axis of ecological cell)
            - y (y-axis of ecological cell)
            - z (z-axis of ecological cell)
            - generation (generation count)
            - key (parameter name)
            - value (parameter value)

        @param start_time: Start time of simulation, which is used as 
        primary key to extract data and results pertaining to the 
        simulation.
        @type start_time: String
        @param x: x-axis of ecological cell.
        @type x: Integer
        @param y: y-axis of ecological cell.
        @type y: Integer
        @param z: z-axis of ecological cell.
        @type z: Integer
        @return: Pandas dataframe containing results.
        """
        sqlstmt = "SELECT distinct generation, key, value from world where start_time = '%s' and x = '%s' and y = '%s' and z = '%s'" % (str(start_time), str(x), str(y), str(z))
        dataframe = self._ExecuteSQL(sqlstmt, "WPTCell")
        dataframe["start_time"] = start_time
        dataframe["x"] = x
        dataframe["y"] = y
        dataframe["z"] = z
        column_names = ["start_time", "x", "y", "z", 
                        "generation", "key", "value"]
        return dataframe.reindex(columns=column_names)

    def WorldParam_TimeCellName(self, start_time, x, y, z, parameter):
        """!
        Method to list the values of a specific parameter of a specific 
        ecological cell of a given simulation (by start_time). Logged 
        operation type = WPTCN.

        Returned Pandas dataframe columns:
            - start_time (start time of simulation, which is used as 
            primary key to extract data and results pertaining to the 
            simulation)
            - x (x-axis of ecological cell)
            - y (y-axis of ecological cell)
            - z (z-axis of ecological cell)
            - generation (generation count)
            - key (parameter name)
            - value (parameter value)

        @param start_time: Start time of simulation, which is used as 
        primary key to extract data and results pertaining to the 
        simulation.
        @type start_time: String
        @param x: x-axis of ecological cell.
        @type x: Integer
        @param y: y-axis of ecological cell.
        @type y: Integer
        @param z: z-axis of ecological cell.
        @type z: Integer
        @param parameter: Required parameter value.
        @type parameter: String
        @return: Pandas dataframe containing results.
        """
        sqlstmt = "SELECT distinct generation, value from world where start_time = '%s' and x = '%s' and y = '%s' and z = '%s' and key = '%s'" % (str(start_time), str(x), str(y), str(z), str(parameter))
        dataframe = self._ExecuteSQL(sqlstmt, "WPTCN")
        dataframe["start_time"] = start_time
        dataframe["key"] = parameter
        dataframe["x"] = x
        dataframe["y"] = y
        dataframe["z"] = z
        column_names = ["start_time", "x", "y", "z", 
                        "generation", "key", "value"]
        return dataframe.reindex(columns=column_names)
    ##################################################################
    # (End of) World Parameters (Table = world) Getter
    ##################################################################

    ##################################################################
    # 5. Organisms Parameters (Table = organisms) Getter
    ##################################################################
    def OrgParam_Time(self, start_time):
        """!
        Method to list organism data for a simulation (by start_time). 
        Logged operation type = OPTime.

        Returned Pandas dataframe columns:
            - start_time (start time of simulation, which is used as 
            primary key to extract data and results pertaining to the 
            simulation)
            - pop_name (population name)
            - org_name (organism name)
            - generation (generation count)
            - key (parameter name)
            - value (parameter value)

        @param start_time: Start time of simulation, which is used as 
        primary key to extract data and results pertaining to the 
        simulation
        @type start_time: String
        @return: Pandas dataframe containing results.
        """
        sqlstmt = "SELECT distinct pop_name, org_name, generation, key, value from organisms where start_time = '%s'" % (str(start_time))
        dataframe = self._ExecuteSQL(sqlstmt, "OPTime")
        dataframe["start_time"] = start_time
        column_names = ["start_time", "pop_name", "org_name", 
                        "generation", "key", "value"]
        return dataframe.reindex(columns=column_names)

    def OrgParam_Pop(self, pop_name):
        """!
        Method to list organism data for a population (by pop_name). 
        Logged operation type = OPPN.

        Returned Pandas dataframe columns:
            - start_time (start time of simulation, which is used as 
            primary key to extract data and results pertaining to the 
            simulation)
            - pop_name (population name)
            - org_name (organism name)
            - generation (generation count)
            - key (parameter name)
            - value (parameter value)

        @param pop_name: Name of the population.
        @type pop_name: String
        @return: Pandas dataframe containing results.
        """
        sqlstmt = "SELECT distinct start_time, org_name, generation, key, value from organisms where pop_name = '%s'" % (str(pop_name))
        dataframe = self._ExecuteSQL(sqlstmt, "OPPN")
        dataframe["pop_name"] = pop_name
        column_names = ["start_time", "pop_name", "org_name", 
                        "generation", "key", "value"]
        return dataframe.reindex(columns=column_names)

    def OrgParam_TimePop(self, start_time, pop_name):
        """!
        Method to list organism data for a population within a simulation.
        Logged operation type = OPTP.

        Returned Pandas dataframe columns:
            - start_time (start time of simulation, which is used as 
            primary key to extract data and results pertaining to the 
            simulation)
            - pop_name (population name)
            - org_name (organism name)
            - generation (generation count)
            - key (parameter name)
            - value (parameter value)

        @param start_time: Start time of simulation, which is used as 
        primary key to extract data and results pertaining to the 
        simulation
        @type start_time: String
        @param pop_name: Name of the population.
        @type pop_name: String
        @return: Pandas dataframe containing results.
        """
        sqlstmt = "SELECT distinct org_name, generation, key, value from organisms where start_time = '%s' and pop_name = '%s'" % (str(start_time), str(pop_name))
        dataframe = self._ExecuteSQL(sqlstmt, "OPTP")
        dataframe["start_time"] = start_time
        dataframe["pop_name"] = pop_name
        column_names = ["start_time", "pop_name", "org_name", 
                        "generation", "key", "value"]
        return dataframe.reindex(columns=column_names)

    def OrgParam_TimePopName(self, start_time, pop_name, parameter):
        """!
        Method to list specific organism parameter for a population 
        within a simulation.
        Logged operation type = OPTPN.

        Returned Pandas dataframe columns:
            - start_time (start time of simulation, which is used as 
            primary key to extract data and results pertaining to the 
            simulation)
            - pop_name (population name)
            - org_name (organism name)
            - generation (generation count)
            - key (parameter name)
            - value (parameter value)

        @param start_time: Start time of simulation, which is used as 
        primary key to extract data and results pertaining to the 
        simulation
        @type start_time: String
        @param pop_name: Name of the population.
        @type pop_name: String
        @param parameter: Required parameter value.
        @type parameter: String
        @return: Pandas dataframe containing results.
        """
        sqlstmt = "SELECT distinct org_name, generation, value from organisms where start_time = '%s' and pop_name = '%s' and key = '%s'" % (str(start_time), str(pop_name), str(parameter))
        dataframe = self._ExecuteSQL(sqlstmt, "OPTPN")
        dataframe["start_time"] = start_time
        dataframe["pop_name"] = pop_name
        dataframe["key"] = parameter
        column_names = ["start_time", "pop_name", "org_name", 
                        "generation", "key", "value"]
        return dataframe.reindex(columns=column_names)
    ##################################################################
    # (End of) Organisms Parameters (Table = organisms) Getter
    ##################################################################

    ##################################################################
    # 6. Miscellaneous Parameters (Table = miscellaneous) Getter
    ##################################################################
    def MiscParam_Time(self, start_time):
        """!
        Method to list miscellaneous parameters of a given simulation 
        (by start_time). Logged operation type = MPTime.

        Returned Pandas dataframe columns:
            - start_time (start time of simulation, which is used as 
            primary key to extract data and results pertaining to the 
            simulation)
            - x (x-axis of ecological cell)
            - y (y-axis of ecological cell)
            - z (z-axis of ecological cell)
            - generation (generation count)
            - key (parameter name)
            - value (parameter value)

        @param start_time: Start time of simulation, which is used as 
        primary key to extract data and results pertaining to the 
        simulation
        @type start_time: String
        @return: Pandas dataframe containing results.
        """
        sqlstmt = "SELECT distinct generation, key, value from miscellaneous where start_time = '%s'" % str(start_time)
        dataframe = self._ExecuteSQL(sqlstmt, "MPTime")
        dataframe["start_time"] = start_time
        dataframe["x"] = None
        dataframe["y"] = None
        dataframe["z"] = None
        column_names = ["start_time", "x", "y", "z", 
                        "generation", "key", "value"]
        return dataframe.reindex(columns=column_names)

    def MiscParam_TimeName(self, start_time, parameter):
        """!
        Method to list specific world parameters of a given simulation 
        (by start_time). Logged operation type = MPTN.

        Returned Pandas dataframe columns:
            - start_time (start time of simulation, which is used as 
            primary key to extract data and results pertaining to the 
            simulation)
            - x (x-axis of ecological cell)
            - y (y-axis of ecological cell)
            - z (z-axis of ecological cell)
            - generation (generation count)
            - key (parameter name)
            - value (parameter value)

        @param start_time: Start time of simulation, which is used as 
        primary key to extract data and results pertaining to the 
        simulation
        @type start_time: String
        @param parameter: Required parameter value.
        @type parameter: String
        @return: Pandas dataframe containing results.
        """
        sqlstmt = "SELECT distinct generation, value from miscellaneous where start_time = '%s' and key = '%s'" % (str(start_time), str(parameter))
        dataframe = self._ExecuteSQL(sqlstmt, "MPTN")
        dataframe["start_time"] = start_time
        dataframe["key"] = parameter
        dataframe["x"] = None
        dataframe["y"] = None
        dataframe["z"] = None
        column_names = ["start_time", "x", "y", "z", 
                        "generation", "key", "value"]
        return dataframe.reindex(columns=column_names)
    ##################################################################
    # (End of) Miscellaneous Parameters (Table = miscellaneous) Getter
    ##################################################################

def FindConstantColumns(dataframe):
    """!
    Function to identify columns with constant value.

    @param dataframe: Pandas dataframe to process.
    @return: List of column names with constant value.
    """
    constantCols = [c for c in dataframe.columns 
                        if len(set(dataframe[c])) == 1]
    return constantCols

def RemoveColumn(dataframe, column_name):
    """!
    Function to remove / drop a column from data frame.

    @param dataframe: Pandas data frame to process.
    @param column_name: Column to remove / drop.
    @type column_name: String
    @return: Reduced Pandas data frame
    """
    return dataframe.drop(column_name, 1)

def SaveDataframe(dataframe, filepath, format="xlsx"):
    """!
    Function to save a data frame into a file.

    @param dataframe: Pandas data frame to save.
    @param filepath: Relative or absolute file path to save.
    @type filepath: String
    @param format: Type of format to save as. Allowable types are 
    "xlsx" (Microsoft Excel), "csv" (comma-separated values). 
    Default = xlsx.
    @type format: String
    """
    filepath = os.path.abspath(filepath)
    if format.lower() == "xlsx": 
        dataframe.to_excel(filepath, index=False)
    elif format.lower() == "csv": 
        dataframe.to_csv(filepath, index=False)
    print("Data saved as %s format into %s" % (format, filepath))

def GenerateFitness(fitnessFunction, simSet, DOSEdb, **fitF):
    """!
    Runner function to generate fitness score table using given fitness 
    function(**fitF). Depending on simSet, multiple replicates of the 
    same simulation can be processed.

    @param fitnessFunction: User-defined function for fitness 
    calculation of one replicate.
    @type fitnessFunction: Function
    @param simSet: Dictionary of {<start_time>: <replicate>}
    @type simSet: Dictionary
    @param DOSEdb: dossier.DOSE_Result_Database object
    @type DOSEdb: Object
    @return: Pandas dataframe of {Replicate, Generation, DO(1), ..., DO(n)}
    """
    fitnessTables = []
    for sim_time in simSet:
        print("Processing simulation start time %s as replicate %s" % \
            (str(sim_time), str(simSet[sim_time])))
        simDF = DOSEdb.OrgParam_Time(sim_time)
        fTable = fitnessFunction(simDF, simSet[sim_time], fitF)
        org_count = max([len(x)-2 for x in fTable])
        columns = ["Replicate", "Generation"] + \
                  ["DO" + str(i+1) for i in range(org_count)]
        fDF = pd.DataFrame(fTable, columns=columns)
        fitnessTables.append(fDF)
    fitnessDF = pd.concat(fitnessTables, ignore_index=True)
    return fitnessDF

def SubsequenceCounter(dataframe, replicate, kwargs):
    """!
    Fitness Function for generateFitness() - Fitness score = number of 
    subsequences in the first chromosome.

    @param dataframe: Returned dataframe from dossier.
    DOSE_Result_Database.OrgParam_Time()
    @param replicate: Replicate number
    @type replicate: Integer
    @param kwargs: Keyword parameters used for fitness calculation.
    @return: [Replicate, Generation, DO(1), ..., DO(n)] of fitness 
    scores.
    """
    subsequence = kwargs["subsequence"]
    generations = list(set(dataframe["generation"].tolist()))
    generations.sort()
    fitnessTable = []
    for gen_count in generations:
        dataDF = dataframe[(dataframe["generation"] == gen_count) & \
                           (dataframe["key"] == "chromosome_0")]
        fScore = [replicate, gen_count] + \
                 [row["value"].count(subsequence)
                    for index, row in dataDF.iterrows()]
        fitnessTable.append(fScore)
    return fitnessTable

def LocalEfficiency(dataframe, replicate, kwargs):
    """!
    Fitness Function for generateFitness() - Fitness score = local efficiency 
    scores of the first chromosome.

    @param dataframe: Returned dataframe from dossier.
    DOSE_Result_Database.OrgParam_Time()
    @param replicate: Replicate number
    @type replicate: Integer
    @param kwargs: Keyword parameters used for fitness calculation.
    @return: [Replicate, Generation, DO(1), ..., DO(n)] of fitness 
    scores.
    """
    enzymatic_reactions = kwargs["enzymatic_reactions"]
    generations = list(set(dataframe["generation"].tolist()))
    generations.sort()
    fitnessTable = []
    def _core(sequence, enzymatic_reactions):
        reactions = []
        for nucleotide in range(0, len(sequence), 2):
            if sequence[nucleotide:nucleotide+2] in enzymatic_reactions.keys():
                reactions.append(enzymatic_reactions[sequence[nucleotide:nucleotide+2]])
            else:
                pass
        G = nx.Graph()
        G.add_edges_from([r for r in reactions])
        return nx.local_efficiency(G)
    for gen_count in generations:
        dataDF = dataframe[(dataframe["generation"] == gen_count) & \
                           (dataframe["key"] == "chromosome_0")]
        fScore = [replicate, gen_count] + \
                 [_core(row["value"], enzymatic_reactions)
                    for index, row in dataDF.iterrows()]
        fitnessTable.append(fScore)
    return fitnessTable

def GlobalEfficiency(dataframe, replicate, kwargs):
    """!
    Fitness Function for generateFitness() - Fitness score = global efficiency 
    scores of the first chromosome.

    @param dataframe: Returned dataframe from dossier.
    DOSE_Result_Database.OrgParam_Time()
    @param replicate: Replicate number
    @type replicate: Integer
    @param kwargs: Keyword parameters used for fitness calculation.
    @return: [Replicate, Generation, DO(1), ..., DO(n)] of fitness 
    scores.
    """
    enzymatic_reactions = kwargs["enzymatic_reactions"]
    generations = list(set(dataframe["generation"].tolist()))
    generations.sort()
    fitnessTable = []
    def _core(sequence, enzymatic_reactions):
        reactions = []
        for nucleotide in range(0, len(sequence), 2):
            if sequence[nucleotide:nucleotide+2] in enzymatic_reactions.keys():
                reactions.append(enzymatic_reactions[sequence[nucleotide:nucleotide+2]])
            else:
                pass
        G = nx.Graph()
        G.add_edges_from([r for r in reactions])
        return nx.global_efficiency(G)
    for gen_count in generations:
        dataDF = dataframe[(dataframe["generation"] == gen_count) & \
                           (dataframe["key"] == "chromosome_0")]
        fScore = [replicate, gen_count] + \
                 [_core(row["value"], enzymatic_reactions)
                    for index, row in dataDF.iterrows()]
        fitnessTable.append(fScore)
    return fitnessTable

def PerceptionSum(dataframe, replicate, kwargs):
    """!
    Fitness Function for generateFitness() - Fitness score = sum of perception 
    genes for the first chromosome.

    @param dataframe: Returned dataframe from dossier.
    DOSE_Result_Database.OrgParam_Time()
    @param replicate: Replicate number
    @type replicate: Integer
    @param kwargs: Keyword parameters used for fitness calculation.
    @return: [Replicate, Generation, DO(1), ..., DO(n)] of fitness 
    scores.
    """
    perception_genes = kwargs["perception_genes"]
    generations = list(set(dataframe["generation"].tolist()))
    generations.sort()
    fitnessTable = []
    def _core(sequence, perception_genes):
        perception_sum = 0
        for nucleotide in range(0, len(sequence), 2):
            if sequence[nucleotide:nucleotide+2] in perception_genes:
                perception_sum += 1
            else:
                pass
        return perception_sum
    for gen_count in generations:
        dataDF = dataframe[(dataframe["generation"] == gen_count) & \
                           (dataframe["key"] == "chromosome_0")]
        fScore = [replicate, gen_count] + \
                 [_core(row["value"], perception_genes)
                    for index, row in dataDF.iterrows()]
        fitnessTable.append(fScore)
    return fitnessTable

def EnzymaticSum(dataframe, replicate, kwargs):
    """!
    Fitness Function for generateFitness() - Fitness score = sum of enzymatic 
    genes for the first chromosome.

    @param dataframe: Returned dataframe from dossier.
    DOSE_Result_Database.OrgParam_Time()
    @param replicate: Replicate number
    @type replicate: Integer
    @param kwargs: Keyword parameters used for fitness calculation.
    @return: [Replicate, Generation, DO(1), ..., DO(n)] of fitness 
    scores.
    """
    enzymatic_genes = kwargs["enzymatic_genes"]
    generations = list(set(dataframe["generation"].tolist()))
    generations.sort()
    fitnessTable = []
    def _core(sequence, enzymatic_genes):
        enzymatic_sum = 0
        for nucleotide in range(0, len(sequence), 2):
            if sequence[nucleotide:nucleotide+2] in enzymatic_genes:
                enzymatic_sum += 1
            else:
                pass
        return enzymatic_sum
    for gen_count in generations:
        dataDF = dataframe[(dataframe["generation"] == gen_count) & \
                           (dataframe["key"] == "chromosome_0")]
        fScore = [replicate, gen_count] + \
                 [_core(row["value"], enzymatic_genes)
                    for index, row in dataDF.iterrows()]
        fitnessTable.append(fScore)
    return fitnessTable
