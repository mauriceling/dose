"""!
Example 03 of DOSSIER [Functions to Analyze Simulation Results 
Database and Periodic Archives from DOSE (Digital Organism Simulation 
Environment) Simulations] - Organism Parameters. 

Date created: 9th July 2021
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

print("OPERATION: Get the organism parameters for " + start_time)
dataframe = db.OrgParam_Time(start_time)
print("SQL statement used: %s" % db.last_sql_statement)
print(dataframe)
print("")

print("OPERATION: Get the organism parameters for pop_01")
dataframe = db.OrgParam_Pop("pop_01")
print("SQL statement used: %s" % db.last_sql_statement)
print(dataframe)
print("")

print("OPERATION: Get the organism parameters for pop_01 of " + start_time)
dataframe = db.OrgParam_TimePop(start_time, "pop_01")
print("SQL statement used: %s" % db.last_sql_statement)
print(dataframe)
print("")

print("OPERATION: Get the organism chromosome_0 for pop_01 of " + start_time)
dataframe = db.OrgParam_TimePopName(start_time, "pop_01", "chromosome_0")
print("SQL statement used: %s" % db.last_sql_statement)
print(dataframe)
print("")

print("Listing of SQL Statements Used")
for k in db.sql_statements:
    print("%i : %s" % (k, db.sql_statements[k]))
