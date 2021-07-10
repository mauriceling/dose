"""!
Example 04 of DOSSIER [Functions to Analyze Simulation Results 
Database and Periodic Archives from DOSE (Digital Organism Simulation 
Environment) Simulations] - Process Fitness Scores. 

Date created: 10th July 2021
"""
import dossier

print("OPERATION: Connect to a DOSE simulation results database")
db = dossier.ConnectDB("Simulations\\simulation.db")
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

fitnessFunction = dossier.subsequenceCounter
fitnessDF = dossier.generateFitness(fitnessFunction, simSet, db, 
                                    subsequence="AA")
print("Fitness Score Data Frame ..............................")
print(fitnessDF)
