"""!
Example 08 of DOSSIER [Functions to Analyze Simulation Results 
Database and Periodic Archives from DOSE (Digital Organism Simulation 
Environment) Simulations] - Process Sum of Enzymatic Genes. 

Date created: 5th August 2021
"""
try: 
    import run_examples_without_installation
except ImportError: pass

import dossier
import sunanda_metabolism as metab

print("OPERATION: Connect to a DOSE simulation results database")
db = dossier.ConnectDB("..//Simulations//simulation.db")
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

fitnessFunction = dossier.MeasureSum
fitnessDF = dossier.GenerateFitness(fitnessFunction, simSet, db, 
                                    measure=metab.enzymatic_genes,
                                    len_of_measure=2)
print("Fitness Score Data Frame ..............................")
print(fitnessDF)

dossier.SaveDataframe(fitnessDF, "dossier_example_08.csv", "csv")
dossier.SaveDataframe(fitnessDF, "dossier_example_08.xlsx", "xlsx")
