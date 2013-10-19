# needed to run this example without prior
# installation of DOSE into Python site-packages
import run_examples_without_installation

# Example codes starts from here
import database_calls as d

(con, cur) = d.connect_database('Simulations/case_study_01.db')

# alternative: start_time = d.db_list_simulations(cur)[0][0]
start_time = d.db_list_simulations(cur, 'parameters')[0][0]

# alternative: generations = d.db_list_generations(cur, start_time)
generations = d.db_list_generations(cur, start_time, 'organisms')

# alternative: datafields = d.db_list_datafields(cur, start_time)
datafields = d.db_list_datafields(cur, start_time, 'organisms')

print "Get entire World.ecosystem, datafields='all', generation=['900']"
ecosys = d.db_get_ecosystem(cur, start_time, 'all', ['900'])
for x in ecosys['900'].keys():
    for y in ecosys['900'][x].keys():
        for z in ecosys['900'][x][y].keys():
            print x, y, z, ecosys['900'][x][y][z]
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
            print x, y, z, ecosys['900'][x][y][z]
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