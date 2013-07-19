'''
World structure for DOSE (digital organism simulation environment)
Date created: 13th September 2012
Licence: Python Software Foundation License version 2 

Reference: Ling, MHT. 2012. An Artificial Life Simulation Library Based on 
Genetic Algorithm, 3-Character Genetic Code and Biological Hierarchy. The 
Python Papers 7: 5.
'''
import copy

class World(object):
    '''
    Representation of a 3-dimensional ecological world.
    
    The ecosystem is made up of ecological cells. Each ecological cell is
    modelled as a dictionary of 
        - local_input: A list containing processed input, representing 
          the partial local ecological condition, to be used as input to 
          the organisms in the current ecological cell. This is updated 
          by World.update_local function.
        - local_output: A list containing processed output, representing 
          the partial local ecological condition. This is updated by 
          World.update_local function.
        - temporary_input: A list acting as temporary holding for input 
          after being fed to the organisms in the current ecological 
          cell, which is to be used to update local_input and local_output 
          lists by World.update_local and World.update_ecology functions.
        - temporary_output: A list acting as temporary holding for output 
          from the organisms in the current ecological cell, which is to 
          be used to update local_input and local_output lists by 
          World.update_local and World.update_ecology functions.
        - organisms: The number of organisms in the current ecological 
          cell which is updated by World.organism_movement and 
          World.organism_location functions.
        
    @see: Ling, MHT. 2012. An Artificial Life Simulation Library Based on 
    Genetic Algorithm, 3-Character Genetic Code and Biological Hierarchy. 
    The Python Papers 7: 5.
    '''
    ecosystem = {}
    
    def __init__(self, world_x, world_y, world_z):
        '''
        Setting up the world and ecosystem
        
        @param world_x: number of ecological cells on the x-axis
        @type world_x: integer
        @param world_y: number of ecological cells on the y-axis
        @type world_y: integer
        @param world_z: number of ecological cells on the z-axis
        @type world_z: integer
        '''
        eco_cell = {'local_input': [], 'local_output': [],
                    'temporary_input': [], 'temporary_output': [],
                    'organisms': 0}
        self.world_x = int(world_x)
        self.world_y = int(world_y)
        self.world_z = int(world_z)
        for x in range(self.world_x):
            eco_x = {}
            for y in range(self.world_y):
                eco_y = {}
                for z in range(self.world_z): 
                    eco_y[z] = copy.deepcopy(eco_cell)
                eco_x[y] = copy.deepcopy(eco_y)
            self.ecosystem[x] = copy.deepcopy(eco_x)
    
    def eco_burial(self, filename):
        '''
        Function to preserve the entire ecosystem.
        
        @param filename: file name of preserved ecosystem.
        '''
        import cPickle
        f = open(filename, 'w')
        cPickle.dump(self.ecosystem, f)
        f.close()
        
    def eco_excavate(self, filename):
        '''
        Function to excavate entire ecosystem.
        
        @param filename: file name of preserved ecosystem.
        '''
        import cPickle
        self.ecosystem = cPickle.load(open(filename, 'r'))
        
    def ecoregulate(self):
        '''
        Function to simulate events to the entire ecosystem. B{This 
        function may be over-ridden by the inherited class or substituted 
        to cater for ecological schemes but not an absolute requirement 
        to do so.}
        '''
        pass
        
    def organism_movement(self, x, y, z): 
        '''
        Function to trigger organism movement from current ecological cell
        to an adjacent ecological cell. B{This function may be over-ridden 
        by the inherited class or substituted to cater for mobility 
        schemes but not an absolute requirement to do so.}
        
        @param x: location of current ecological cell on the x-axis
        @type x: integer
        @param y: location of current ecological cell on the y-axis
        @type y: integer
        @param z: location of current ecological cell on the z-axis
        @type z: integer
        '''
        pass
    def organism_location(self, x, y, z): 
        '''
        Function to trigger organism movement from current ecological cell
        to a distant ecological cell. B{This function may be over-ridden 
        by the inherited class or substituted to cater for mobility 
        schemes but not an absolute requirement to do so.}
        
        @param x: location of current ecological cell on the x-axis
        @type x: integer
        @param y: location of current ecological cell on the y-axis
        @type y: integer
        @param z: location of current ecological cell on the z-axis
        @type z: integer
        '''
        pass
    
    def update_ecology(self, x, y, z): 
        '''
        Function to process temporary_input and temporary_output from the 
        activities of the organisms in the current ecological cell into a 
        local ecological cell condition, and update the ecosystem.
        B{This function may be over-ridden by the inherited class or 
        substituted to cater for ecological schemes but not an absolute 
        requirement to do so.}
        
        @param x: location of current ecological cell on the x-axis
        @type x: integer
        @param y: location of current ecological cell on the y-axis
        @type y: integer
        @param z: location of current ecological cell on the z-axis
        @type z: integer
        '''
        pass
        
    def update_local(self, x, y, z): 
        '''
        Function to update local ecological cell condition from the 
        ecosystem.
        B{This function may be over-ridden by the inherited class or 
        substituted to cater for ecological schemes but not an absolute 
        requirement to do so.}
        
        @param x: location of current ecological cell on the x-axis
        @type x: integer
        @param y: location of current ecological cell on the y-axis
        @type y: integer
        @param z: location of current ecological cell on the z-axis
        @type z: integer
        '''
        pass
        
    def report(self):
        '''
        Function to report the status of the world and ecosystem. B{This 
        function may be over-ridden by the inherited class or substituted 
        to cater for specific reporting schemes but not an absolute 
        requirement to do so.} 
        
        @return: dictionary of status describing the current generation
        '''
        pass
        