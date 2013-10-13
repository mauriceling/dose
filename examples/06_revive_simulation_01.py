# needed to run this example without prior
# installation of DOSE into Python site-packages
import run_examples_without_installation

# Example codes starts from here
import dose

rev_parameters = {'sim_folder' : '\Simulations\\01_basic_functions_one_cell_deployment_2013-10-12-1381600853.53\\',
                  'eco_file' : '01_basic_functions_one_cell_deployment_gen100.eco', 
                  'pop_files' : ['01_basic_functions_one_cell_deployment_pop_01_100_100.gap'],
                  'generations' : 50}

dose.revive_simulation(rev_parameters)