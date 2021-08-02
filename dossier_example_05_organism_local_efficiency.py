"""!
Example 05 of DOSSIER [Functions to Analyze Simulation Results 
Database and Periodic Archives from DOSE (Digital Organism Simulation 
Environment) Simulations] - Process Local Efficiency Scores. 

Date created: 1st August 2021
"""
import dossier

print("OPERATION: Connect to a DOSE simulation results database")
db = dossier.ConnectDB("Simulations//control_simulation_high_mutation.db")
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

fitnessFunction = dossier.LocalEfficiency
fitnessDF = dossier.GenerateFitness(fitnessFunction, simSet, db, 
                                    subsequence="AA")
print("Fitness Score Data Frame ..............................")
print(fitnessDF)

dossier.SaveDataframe(fitnessDF, "dossier_example_05.csv", "csv")
dossier.SaveDataframe(fitnessDF, "dossier_example_05.xlsx", "xlsx")
