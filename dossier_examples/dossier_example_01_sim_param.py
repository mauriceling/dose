"""!
Example 01 of DOSSIER [Functions to Analyze Simulation Results 
Database and Periodic Archives from DOSE (Digital Organism Simulation 
Environment) Simulations] - Simulation Parameters. 

Date created: 17th April 2021
"""
# needed to run this example without prior
# installation of DOSE into Python site-packages
try: 
    import run_examples_without_installation
except ImportError: pass

import dossier

print("OPERATION: Connect to a DOSE simulation results database")
db = dossier.ConnectDB("..\\Simulations\\simulation.db")
print("")

print("OPERATION: List available simulation results")
dataframe = db.Sims()
print("SQL statement used: %s" % db.last_sql_statement)
start_time = dataframe.iloc[0]['start_time']
print(dataframe)
print("")
print("From now on, we will be using simulation " + start_time)
print("")

print("OPERATION: List the parameter types in parameters table")
resultList = db.ParamTypes("parameters")
print("SQL statement used: %s" % db.last_sql_statement)
print(resultList)
print("")

print("OPERATION: List the parameter types in world table")
resultList = db.ParamTypes("world")
print("SQL statement used: %s" % db.last_sql_statement)
print(resultList)
print("")

print("OPERATION: List the parameter types in organisms table")
resultList = db.ParamTypes("organisms")
print("SQL statement used: %s" % db.last_sql_statement)
print(resultList)
print("")

print("OPERATION: List the parameter types in miscellaneous table")
resultList = db.ParamTypes("miscellaneous")
print("SQL statement used: %s" % db.last_sql_statement)
print(resultList)
print("")

print("OPERATION: List simulation parameters for " + start_time + \
    " except interpreter and deployment scheme")
dataframe = db.SimParam_Time(start_time)
print("SQL statement used: %s" % db.last_sql_statement)
print(dataframe)
print("")

print("OPERATION: Get the value of background_mutation")
dataframe = db.SimParam_Name("background_mutation")
print("SQL statement used: %s" % db.last_sql_statement)
print(dataframe)
print("")

print("OPERATION: Get the value of background_mutation for " + start_time)
value = db.SimParam_TimeName(start_time, "background_mutation")
print("SQL statement used: %s" % db.last_sql_statement)
print(value)
print("")

print("Listing of SQL Statements Used")
for k in db.sql_statements:
    print("%i : %s" % (k, db.sql_statements[k]))
