'''
Example 07: Extracting data from simulation logging database
'''
# needed to run this example without prior
# installation of DOSE into Python site-packages
try: 
	import run_examples_without_installation
except ImportError: pass

# Example codes starts from here
import dose.database_calls as d

print "Connecting to logging database"
(con, cur) = d.connect_database('Simulations/case_study_01.db')

print "Get simulations"
# alternative: start_time = d.db_list_simulations(cur)[0][0]
start_time = d.db_list_simulations(cur, 'parameters')[0][0]
print "simulation start time:", start_time

print "Get logged generations in one of the logged simulations"
# alternative: generations = d.db_list_generations(cur, start_time)
generations = d.db_list_generations(cur, start_time, 'organisms')
print "number of logged generations:", len(generations)
print

print "Get logged populations (by population names) in one of the logged \
simulations"
population_names = d.db_list_population_name(cur, start_time)
print "logged populations:", population_names
print

print "Get logged organism's data fields in one of the logged simulations"
# alternative: datafields = d.db_list_datafields(cur, start_time)
datafields = d.db_list_datafields(cur, start_time, 'organisms')
print 'logged datafields in organism:', datafields

print "Get entire World.ecosystem, datafields='all', generation=['900']"
ecosys = d.db_get_ecosystem(cur, start_time, 'all', ['900'])
for x in ecosys['900'].keys():
    for y in ecosys['900'][x].keys():
        for z in ecosys['900'][x][y].keys():
            print '900', x, y, z, ecosys['900'][x][y][z]
print
print

print "Get entire World.ecosystem, datafields='all', generation=['100', '200', '300']"
ecosys = d.db_get_ecosystem(cur, start_time, 'all', ['100', '200', '300'])
for gen in ecosys.keys():
    for x in ecosys[gen].keys():
        for y in ecosys[gen][x].keys():
            for z in ecosys[gen][x][y].keys():
                print gen, x, y, z, ecosys[gen][x][y][z]
print
print

print "Get entire World.ecosystem, datafields='organisms', generation=['900']"
ecosys = d.db_get_ecosystem(cur, start_time, 'organisms', ['900'])
for x in ecosys['900'].keys():
    for y in ecosys['900'][x].keys():
        for z in ecosys['900'][x][y].keys():
            print '900', x, y, z, ecosys['900'][x][y][z]
print
print

print "Get entire World.ecosystem, datafields='all', generation=['900', '300']"
ecosys = d.db_get_ecosystem(cur, start_time, 'all', ['900', '300'])
for gen in ecosys.keys():
    for x in ecosys[gen].keys():
        for y in ecosys[gen][x].keys():
            for z in ecosys[gen][x][y].keys():
                print gen, x, y, z, ecosys[gen][x][y][z]
print
print

print "Get entire Organism.status dictionary, datafields='all', \
generation=['900']"
status = d.db_get_organisms_status(cur, start_time, population_names[0], 
                                 'all', ['900'])
for identity in status['900'].keys():
    for key in status['900'][identity].keys():
        print '900', identity, key, status['900'][identity][key]
print
print

print "Get entire Organism.status dictionary, datafields='all', \
generation=['300', '900']"
status = d.db_get_organisms_status(cur, start_time, population_names[0], 
                                 'all', ['300', '900'])
for gen in status.keys():
    for identity in status[gen].keys():
        for key in status[gen][identity].keys():
            print gen, identity, key, status[gen][identity][key]
print
print

print "Get entire Organism.status dictionary, datafields='identity', \
generation=['900']"
status = d.db_get_organisms_status(cur, start_time, population_names[0], 
                                 'identity', ['900'])
for identity in status['900'].keys():
    print '900', identity, status['900'][identity]
print
print

print "Get chromosomal sequences for generation=['900']"
sequences = d.db_get_organisms_chromosome_sequences(cur, start_time, 
                                                    population_names[0], 
                                                    ['900'])
for gen in sequences.keys():
    for identity in sequences[gen].keys():
        for chromosome_number in range(len(sequences[gen][identity])):
            print gen, identity, chromosome_number, \
            sequences[gen][identity][chromosome_number]
print
print

print "Get chromosomal sequences for generation=['300', '900']"
sequences = d.db_get_organisms_chromosome_sequences(cur, start_time, 
                                                    population_names[0], 
                                                    ['300', '900'])
for gen in sequences.keys():
    for identity in sequences[gen].keys():
        for chromosome_number in range(len(sequences[gen][identity])):
            print gen, identity, chromosome_number, \
            sequences[gen][identity][chromosome_number]
print
print