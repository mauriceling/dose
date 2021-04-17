"""!
Common Usage of DOSSIER [Functions to Analyze Simulation Results 
Database and Periodic Archives from DOSE (Digital Organism Simulation 
Environment) Simulations]. 

Date created: 17th April 2021
"""
from pprint import pprint

import dossier

print("OPERATION: Connect to a DOSE simulation results database")
db = dossier.connect_db("Simulations\\simulation.db")
print("")

print("OPERATION: List available simulation results")
dataframe = db.list_simulations()
print("SQL statement used: %s" % db.last_sql_statement)
start_time = dataframe.iloc[0]['start_time']
print(dataframe)
print("")
print("From now on, we will be using simulation " + start_time)
print("")

print("OPERATION: List the parameter types in parameters table")
resultList = db.list_parameter_types("parameters")
print("SQL statement used: %s" % db.last_sql_statement)
print(resultList)
print("")

print("OPERATION: List the parameter types in world table")
resultList = db.list_parameter_types("world")
print("SQL statement used: %s" % db.last_sql_statement)
print(resultList)
print("")

print("OPERATION: List the parameter types in organisms table")
resultList = db.list_parameter_types("organisms")
print("SQL statement used: %s" % db.last_sql_statement)
print(resultList)
print("")

print("OPERATION: List the parameter types in miscellaneous table")
resultList = db.list_parameter_types("miscellaneous")
print("SQL statement used: %s" % db.last_sql_statement)
print(resultList)
print("")

print("OPERATION: List simulation parameters for " + start_time + \
    " except interpreter and deployment scheme")
dataframe = db.simulation_parameters(start_time)
print("SQL statement used: %s" % db.last_sql_statement)
print(dataframe)
print("")

pprint(db.sql_statements)