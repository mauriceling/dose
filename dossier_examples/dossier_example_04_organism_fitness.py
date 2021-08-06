"""!
Example 04 of DOSSIER [Functions to Analyze Simulation Results 
Database and Periodic Archives from DOSE (Digital Organism Simulation 
Environment) Simulations] - Process Fitness Scores. 

Date created: 10th July 2021
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

simSet = {}
for index, row in dataframe.iterrows():
    simSet[row["start_time"]] = index
print("simSet = " + str(simSet))

fitnessFunction = dossier.SubsequenceCounter
fitnessDF = dossier.GenerateFitness(fitnessFunction, simSet, db, 
                                    subsequence="AA")
print("Fitness Score Data Frame ..............................")
print(fitnessDF)

dossier.SaveDataframe(fitnessDF, "dossier_example_04.csv", "csv")
dossier.SaveDataframe(fitnessDF, "dossier_example_04.xlsx", "xlsx")
