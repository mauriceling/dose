# needed to run this example without prior
# installation of DOSE into Python site-packages
try: 
	import run_examples_without_installation
except ImportError: pass

# Example codes starts from here
import dose, random
from collections import Counter
from copy import deepcopy

parameters = {"database_source" : "T1_11x0.db",
              "simulation_time": "default",
              "rev_start" : [200],
              "extend_gen" : 5000,
              "simulation_name": "T1_11x0_revival",
              "database_file": "T1_11x0_revival.db",
              "database_logging_frequency": 1,
              }

class simulation_functions(dose.dose_functions):

    def organism_movement(self, Populations, pop_name, World): pass

    def organism_location(self, Populations, pop_name, World): pass

    def ecoregulate(self, World): pass

    def update_ecology(self, World, x, y, z): pass

    def update_local(self, World, x, y, z): pass

    def report(self, World): pass

    def fitness(self, Populations, pop_name):
        for organism in Populations[pop_name].agents:
        	#Fitness Score with Cost

            chromosome = organism.genome[0].sequence
            fitness_cost = (abs(chromosome.count('0') - 250) + abs(chromosome.count('1') - 250)) / 500.0;
            organism.status['fitness_kill'] = 100 - (fitness_cost * 100)

            #Fitness Score
            final_fitness = []
            zero_count = []
            for base_index in xrange(parameters["chromosome_size"] - 1):
                if int(chromosome[base_index]) == 0 and int(chromosome[base_index - 1]) != 0:
                    next_index = 1
                    while int(chromosome[next_index + base_index]) == 0:
                        next_index += 1
                        if (next_index + base_index) == parameters["chromosome_size"]: break
                    zero_count.append(next_index)
            for sequence in xrange(len(zero_count)):
                if len(final_fitness) == 10: break
                seq_score = sorted(zero_count, reverse = True)[sequence]
                if seq_score > int(parameters["goal"]/10): seq_score = int(parameters["goal"]/10)
                final_fitness.append(seq_score)
            organism.status['fitness'] = sum(final_fitness)

    def mutation_scheme(self, organism):
        organism.genome[0].rmutate(parameters["mutation_type"],
                                   parameters["additional_mutation"])

    def prepopulation_control(self, Populations, pop_name): pass

    def mating(self, Populations, pop_name): 
        group = deepcopy(Populations[pop_name].agents)
        for organism in group:
            organism.generate_name()
            Populations[pop_name].agents.append(organism)

    def postpopulation_control(self, Populations, pop_name):
    	#FPS

        group = deepcopy(Populations[pop_name].agents)
        fitness_dict = {}
        for organism in group:
            fitness_dict[organism.status['identity']] = float(organism.status['fitness_kill'])
        sorted_fitness = sorted(list(fitness_dict.items()), key=lambda x: x[1])
        sorted_fitness = [list(item) for item in sorted_fitness]
        total_fitness = sum(fitness_dict.values())
        cumulated_fitness = 0
        for i in range(len(sorted_fitness)):
            sorted_fitness[i][1] = cumulated_fitness + (sorted_fitness[i][1] / total_fitness)
            cumulated_fitness = cumulated_fitness + (sorted_fitness[i][1] / total_fitness)
        filter_list = []
        while len(filter_list) != 100:
            random_val = random.uniform(min([fitness[1] for fitness in sorted_fitness]), 
                                        sum([fitness[1] for fitness in sorted_fitness]))
            for fitness_list in sorted_fitness:
                if fitness_list[1] > random_val and fitness_list[0] not in filter_list:
                    filter_list.append(fitness_list[0])
                    break
        new_population = [organism for organism in Populations[pop_name].agents if organism.status['identity'] in filter_list]
        Populations[pop_name].agents = new_population

    def generation_events(self, Populations, pop_name): pass

    def population_report(self, Populations, pop_name):
        report_list = []
        for organism in Populations[pop_name].agents:
            chromosome = organism.status['identity']
            fitness = str(organism.status['fitness'])
            report_list.append(chromosome + ' ' + fitness)
        return '\n'.join(report_list)

    def database_report(self, con, cur, start_time, 
                        Populations, World, generation_count):
        try:
            dose.database_report_populations(con, cur, start_time, 
                                             Populations, generation_count)
        except: pass
        try:
            dose.database_report_world(con, cur, start_time, 
                                       World, generation_count)
        except: pass

    def deployment_scheme(self, Populations, pop_name, World): pass

for trial in range(1, 26):
    parameters["simulation_name"] = "T" + str(trial) + "_fps_11x0_loss1"
    parameters["database_source"] = "T" + str(trial) + "_fps_11x0_gain1.db"
    parameters["database_file"] = "T" + str(trial) + "_fps_11x0_loss1.db"
    dose.revive_simulation(parameters, simulation_functions)
    parameters["simulation_time"] = "default"