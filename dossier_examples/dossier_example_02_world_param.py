"""!
Example 02 of DOSSIER [Functions to Analyze Simulation Results 
Database and Periodic Archives from DOSE (Digital Organism Simulation 
Environment) Simulations] - World Parameters. 

Date created: 18th April 2021
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

print("OPERATION: Get the world parameters for " + start_time)
dataframe = db.WorldParam_Time(start_time)
print("SQL statement used: %s" % db.last_sql_statement)
print(dataframe)
print("")

print("OPERATION: Get the cell parameters for " + start_time + ", location 0,0,0")
dataframe = db.WorldParam_TimeCell(start_time, 0, 0, 0)
print("SQL statement used: %s" % db.last_sql_statement)
print(dataframe)
print("")

print("OPERATION: Get the organism parameter for " + start_time + ", location 0,0,0")
dataframe = db.WorldParam_TimeCellName(start_time, 0, 0, 0, "organisms")
print("SQL statement used: %s" % db.last_sql_statement)
print(dataframe)
print("")

print("Listing of SQL Statements Used")
for k in db.sql_statements:
    print("%i : %s" % (k, db.sql_statements[k]))
