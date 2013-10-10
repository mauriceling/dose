'''
Parameter file for DOSE simulation.
Date created: 13th September 2012

This file contains the default parameters for DOSE simulation.
'''

'''
Initial chromosome (list) for the ancestor organism
'''
initial_chromosome = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 
'0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 
'0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 
'0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 
'0', '0', '0', '0']

'''
Probability of number of mutations per base. For example, 0.1 means 10% of 
the chromosome will be mutated per generation.
'''
background_mutation_rate = 0.1

'''
Probability of mutation per base above additional_mutation_rate. No mutation 
event will ever happen if (additional_mutation_rate + additional_mutation_rate) 
is less than zero.
'''
additional_mutation_rate = 0

'''
Size of cytoplasm (length of list) for the ancestor organism.
'''
cytoplasm_size = 50

'''
Maximum size of cytoplasm (length of list) allowable. Some Ragaraja instructions
can increase cytoplasms size, equivalent to cell enlargement.
'''
max_cytoplasm_size = 200

'''
If 'True', a clean cytoplasm will be used to execute the genome. If 'False',
the cytoplasm will be reused in the next generation.
'''
clean_cytoplasm = True

'''
Maximum number of codons to evaluate. Therfore, the maximum evaluated genome
is 3*max_codon bases.
'''
max_codon = 2000

'''
List containing name(s) of population. The number of names = the number of 
populations to create. 
'''
population_names = ['pop1', 'pop2']

'''
Number of organism per population.
'''
population_size = 100

'''
Number of ecological cells in the world in (x,y,z) coordinate as 
(world_x, world_y, world_z).
'''
world_x = 5
world_y = 5
world_z = 5

'''
List of tuple indicating the location on ecosystem to map the population(s) and
will be mapped in the same order as population_names. For example, if 
population_names = ['pop1', 'pop2'] and 
population_locations = [(0,0,0), (4,4,4)],
population 'pop1' will be in (0,0,0) and population 'pop2' will be in (4,4,4).
'''
population_locations = [(0,0,0), (4,4,4)]

'''
Maximum number of generations to simulate.
'''
maximum_generations = 500

'''
Number of generations between each freezing/fossilization event.
Freezing/fossilization event is similar to glycerol stocking in microbiology.
'''
fossilized_frequency = 100

'''
Proportion of population to freeze/fossilize. If the population size or the
preserved proportion is below 100, the entire population will be preserved.
'''
fossilized_ratio = 0.01

'''
Dictionary containing prefix of file names for freezing/fossilization. The 
preserved sample will be written into a file with name in the following 
format - <prefix>_<generation count>_<sample size>.gap
'''
fossil_files = {'pop1': 'pop1', 'pop2': 'pop2'}

'''
Number of generations between printing of reports (based on Population.report
function) into files. The result file format is <UTC date time stamp>
<current generation count> <output from Population.report function>.
'''
print_frequency = 10

'''
Dictionary containing file names for result files. File name will be
<file names>.result
'''
result_files = {'pop1': 'pop1', 'pop2': 'pop2'}

'''
Version of Ragaraja instruction set to use.
'''
ragaraja_version = 0.1

'''
File containing Ragaraja instruction set to be used. This option is only
effective when ragaraja_version = 0. Format of file is <instruction>={Y|N}
where "Y" = instruction to be used and "N" = instruction not to be used.
'''
user_defined_instructions = 'ragaraja_instructions.txt'

'''
Number of generations between each burial/preservation of ecosystem.
'''
eco_buried_frequency = 500

'''
Prefix of file name for ecosystem burial/preservation. The preserved ecosystem 
will be written into a file with name in the following format - 
<prefix>_<generation count>.eco
'''
eco_burial_file = 'eco'
