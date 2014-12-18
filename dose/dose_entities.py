'''
Boiler-plate codes for DOSE (digital organism simulation environment) 
entities.
Date created: 13th September 2012

Reference: Ling, MHT. 2012. An Artificial Life Simulation Library Based on 
Genetic Algorithm, 3-Character Genetic Code and Biological Hierarchy. The 
Python Papers 7: 5.
'''

import genetic as g
import dose_world as w
from dose_parameters import initial_chromosome, background_mutation_rate
from dose_parameters import cytoplasm_size, population_size
from dose_parameters import maximum_generations
from dose_parameters import world_x, world_y, world_z

Chromosome = g.Chromosome(initial_chromosome, 
                          ['0','1','2','3','4','5','6','7','8','9'], 
                          background_mutation_rate)
                          
class Organism(g.Organism):
    
    cytoplasm = [0]*cytoplasm_size
    
    def __init__(self): self.genome = [Chromosome.replicate()]
    def get_cytoplasm(self): 
        return ','.join([str(x) for x in self.cytoplasm])
    def fitness(self): pass
    def mutation_scheme(self): pass
        
class Population(g.Population):
    
    def __init__(self, pop_size=population_size, 
                 max_gen=maximum_generations):
        self.agents = [Organism() for x in range(pop_size)]
        self.generation = 0
        self.maximum_generations = max_gen
    def prepopulation_control(self): pass
    def mating(self): pass
    def postpopulation_control(self): pass
    def generation_events(self): pass
    def report(self): pass
    
class World(w.World):
    def __init__(self, world_x=world_x, world_y=world_y, world_z=world_z):
        super(World, self).__init__(world_x, world_y, world_z)
    def organism_movement(self, x, y, z): pass
    def organism_location(self, x, y, z): pass
    def ecoregulate(self): pass
    def update_ecology(self, x, y, z): pass
    def update_local(self, x, y, z): pass
    def report(self): pass
    