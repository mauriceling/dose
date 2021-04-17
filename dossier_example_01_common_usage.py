"""!
Common Usage of DOSSIER [A Library of Utility Functions to Analyze 
Simulation Results Database from DOSE (Digital Organism Simulation 
Environment) Simulations]. 

Date created: 17th April 2021
"""

import dossier

print("OPERATION: Connect to a DOSE simulation results database")
db = dossier.connect_db("Simulations\\simulation.db")
print("")

print("OPERATION: List available simulation results")
dataframe = db.list_simulations()
print("SQL statement used: %s" % db.sql_statements[-1])
start_time = dataframe.iloc[0]['start_time']
print(dataframe)
print("")
print("From now on, we will be using simulation " + start_time)
print("")

print("OPERATION: List simulation parameters for " + start_time + \
    " except interpreter and deployment scheme")
dataframe = db.list_simulation_parameters(start_time)
print("SQL statement used: %s" % db.sql_statements[-1])
print(dataframe)
print("")

