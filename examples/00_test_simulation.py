# needed to run this example without prior
# installation of DOSE into Python site-packages
import run_examples_without_installation

# Example codes starts from here
import dose, genetic, random, os
import simulation_calls as helper
import database_calls

dbpath = os.sep.join([os.getcwd(),
                      'Simulations',
                      "case_study_01"])
(con, cur) = database_calls.connect_database(dbpath, None)

World = database_calls.db_reconstruct_world(cur, '2013-10-19-1382200534.1', 1000)