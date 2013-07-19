'''
Framework for Neural Network Applications
Date created: 10th May 2013
License: Python Software Foundation License version 2
'''
import random
import copy

# -------------------------------------------------------------------
# Transfer functions and its inverse and derivative
# -------------------------------------------------------------------
def tf_linear(x): 
    '''Linear transfer function.
    Equation: y = x'''
    y = x
    return y
    
def itf_linear(y): 
    '''Linear transfer function - inverse.
    Equation: x = y'''
    x = y
    return x
    
def dtf_linear(x): 
    '''Linear transfer function - derivative.
    Equation: df = 1.0'''
    df = 1.0
    return df
# -------------------------------------------------------------------
# END - Transfer functions and its inverse and derivative
# -------------------------------------------------------------------


class Neuron:
    '''
    Class for a Neuron.
    
        1. Each neuron is identified by a unique name, which will be used 
        for mapping between different neurons.
        2. A dictionary, named "cellbody", is provided to contain any 
        other information needed. For example, it can be used to contain 
        a timer for time-delayed neuron activation or it can be used for 
        neuronal memory.
    '''
    name = None
    weights = {}
    cellbody = {}
    transfer_function = None
    itransfer_function = None
    dtransfer_function = None
    
    def __init__(self, name=None, transfer_function=tf_linear,
                 itransfer_function=itf_linear,
                 dtransfer_function=dtf_linear):
        '''
        Constructor method for Neuron class.
        
        @param name: unique name of the neuron. Default = a string of
        60 to 75 numbers.
        @type name: string
        @param transfer_function: a function to convert the consolidated
        weighted input for the neuron and generate an output signal. 
        Default = tf_linear; that is, output signal = consolidated 
        weighted input.
        @type transfer_function: function
        @param itransfer_function: inverse of transfer_function, 
        used by some learning algorithms, Default = itf_linear
        @type itransfer_function: function
        @param dtransfer_function: differential of transfer_function, 
        used by some learning algorithms, Default = dtf_linear
        @type dtransfer_function: function
        '''
        self.transfer_function = transfer_function
        self.dtransfer_function = dtransfer_function
        if name != None:
            self.name = str(name)
        else:
            name = str(int(random.random() * 1e15))
            name = name + str(int(random.random() * 1e15))
            name = name + str(int(random.random() * 1e15))
            name = name + str(int(random.random() * 1e15))
            self.name = name + str(int(random.random() * 1e15))
            
    def generate_name(self):
        '''
        Generate a new random name (a string of 60 to 75 numbers) for
        the current neuron.
        
        @return: new name of neuron.
        '''
        self.name = str(int(random.random() * 1e15)) + \
                    str(int(random.random() * 1e15)) + \
                    str(int(random.random() * 1e15)) + \
                    str(int(random.random() * 1e15)) + \
                    str(int(random.random() * 1e15))
        return self.name
            
    def set_transfer_functions(self, transfer_function,
                               itransfer_function=None,
                               dtransfer_function=None):
        '''
        Set transfer function, its inverse and differential functions.
        
        @param transfer_function: a function to convert the consolidated
        weighted input for the neuron and generate an output signal. 
        @type transfer_function: function
        @param itransfer_function: inverse of transfer_function, 
        used by some learning algorithms, Default = None
        @type itransfer_function: function
        @param dtransfer_function: differential of transfer_function, 
        used by some learning algorithms, Default = None
        @type dtransfer_function: function
        '''
        self.transfer_function = transfer_function
        self.itransfer_function = itransfer_function
        self.dtransfer_function = dtransfer_function
        
    def execute(self, synapses, activations):
        '''
        Execute/activate the neuron into action.
        
        @param synapses: dictionary of reverse synaptic connections and 
        its synaptic weights in the format of {name of signal receiving 
        neuron>: {<name of signal receiving neuron>: <synaptic weight>}}
        @type synapses: dictionary
        @param activations: a dictionary of current activations of the 
        entire network where keys are the names of neurons and values 
        are the activation state or current output signal.
        @type activations: dictionary
        @return: activations dictionary with the updated output signal 
        or activation state from the current neuron.
        '''
        synapses = synapses[self.name]
        synaptic_input = 0.0
        for key in synapses.keys():
            try: 
                synaptic_input = synaptic_input + \
                    (float(synapses[key]) * float(activations[key]))
            except KeyError: pass
        synaptic_input = float(synaptic_input)
        signal = self.transfer_function(synaptic_input)
        activations[self.name] = signal
        return activations
        

# -------------------------------------------------------------------
# Learning algorithms
# -------------------------------------------------------------------

# -------------------------------------------------------------------
# END - Learning algorithms
# -------------------------------------------------------------------


class Brain:
    '''
    Class for the neural network.
    
        1. A brain consists of a set of neurons (uniquely named or 
        uniquely randomly named) held in "neuron_pool" dictionary where 
        key is the name and value is the neuron object.
        2. The corresponding names of neurons are entered into 
        "activations" dictionary as keys. This dictionary holds the 
        current activation states or output signals (as values) of all 
        neurons.
        3. A sequence of neuronal activity is given as activation_sequence, 
        which is a list of list. This suggests that neurons listed in 
        activation_sequence[0] will be activated before those neurons 
        listed in activation_sequence[1], and neuron in 
        activation_sequence[0][0] will be activated before neuron in 
        activation_sequence[0][1]. Inherited class can over-ride 
        Brain.run() method to cater for parallel activations of all 
        neurons in activation_sequence[0] or even parallel activation of 
        all neurons regardless of sequence.
        4. In sequential activation (that is activation_sequence[0] before
        activation_sequence[1]), neurons in activation_sequence[0] will be 
        the input neurons to traditional neural networks.
        5. The connections and synaptic weights are registered in 
        "synapses" dictionary as a reverse connection - {<name of signal 
        receiving neuron>: <dictionary of signal receiving neurons and 
        its weights>} where <dictionary of signal receiving neurons and 
        its weights> is {<name of signal receiving neuron>: 
        <synaptic weight>}. Hence, synpases dictionary is a nested 
        dictionary of {name of signal receiving neuron>: {<name of signal 
        receiving neuron>: <synaptic weight>}}.
        6. A dictionary, called "brainmatter", is provided to contain any 
        other information needed.
        7. The brain will also a learning algorithm to train / learn by 
        itself.
    '''
    activations = {}
    neuron_pool = {}
    synapses = {}
    activation_sequence = []
    brainmatter = {}
    learning_algorithm = None
    
    def __init__(self, number_of_neurons=0, original_neuron=None,
                 list_of_neuron_names=[], learning_algorithm=None):
        '''
        Constructor method for Brain class.
        
        A brain or neural network can be constructed by a predefined 
        list of unique names for neurons or by stating the number of
        neurons required. In both cases, a pre-created neuron may be 
        used but is not mandatory. However, in event where both the 
        list of unique names for neurons and the number of neurons 
        required are given, the list of unique names for neurons takes
        precedence - for example, if 5 neuron names but 10 neurons are
        required, then only 5 neurons (which are named) will be created.
        
        @param number_of_neurons: number of neurons requested (takes a 
        lower precedence than the names of neurons), default = 0.
        @type number_of_neurons: integer
        @param original_neuron: a pre-created neuron to duplicate, 
        default = None
        @type original_neuron: Neuron object
        @param list_of_neuron_names: names for neurons to be created
        (takes a higher precedence than the number of neurons requested), 
        default = [] (empty list).
        @type list_of_neuron_names: list
        @param learning_algorithm: learning mechanism for brain
        @type learning_algorithm: function
        '''
        self.learning_algorithm = learning_algorithm
        if len(list_of_neuron_names) > 0:
            number_of_neurons = len(list_of_neuron_names)
        else:
            number_of_neurons = int(number_of_neurons)
        if (original_neuron == None) and (len(list_of_neuron_names) == 0):
            for x in range(number_of_neurons):
                new_neuron = Neuron()
                self.neuron_pool[new_neuron.name] = new_neuron
                self.activations[new_neuron.name] = 0.0
                self.synapses[new_neuron.name] = {}
        elif (original_neuron == None) and (len(list_of_neuron_names) > 0):
            for name in list_of_neuron_names:
                new_neuron = Neuron()
                new_neuron.name = name
                self.neuron_pool[name] = new_neuron
                self.activations[name] = 0.0
                self.synapses[new_neuron.name] = {}
        elif (original_neuron != None) and (len(list_of_neuron_names) == 0):
            for x in range(number_of_neurons):
                new_neuron = copy.deepcopy(original_neuron)
                self.neuron_pool[new_neuron.name] = new_neuron
                self.activations[new_neuron.name] = 0.0
                self.synapses[new_neuron.name] = {}
        else: # (original_neuron != None) and (len(list_of_neuron_names) > 0)
            for name in list_of_neuron_names:
                new_neuron = copy.deepcopy(original_neuron)
                new_neuron.name = name
                self.neuron_pool[name] = new_neuron
                self.activations[name] = 0.0
                self.synapses[new_neuron.name] = {}
            
    def connect_neurons(self, originating_neuron, destination_neuron):
        '''
        Establish synaptic connection between 2 existing neurons.
        
        @param originating_neuron: name of neuron to connect from
        @type originating_neuron: string
        @param destination_neuron: name of neuron to connect to
        @type destination_neuron: string
        '''
        originating_neuron = str(originating_neuron)
        destination_neuron = str(destination_neuron)
        if originating_neuron not in self.synapses:
            raise AttributeError('Originating neuron name, %s, is not \
            found - this neuron has not been created. Connection can \
            only be established on 2 existing neurons' % 
            originating_neuron)
        elif destination_neuron not in self.synapses:
            raise AttributeError('Destination neuron name, %s, is not \
            found - this neuron has not been created. Connection can \
            only be established on 2 existing neurons' % 
            destination_neuron)
        elif originating_neuron in self.synapses[destination_neuron]:
            raise AttributeError('A connection/synapse had existed \
            between %s and %s. Does nothing.' % (originating_neuron, 
                                                 destination_neuron))
        else:
            self.synapses[destination_neuron][originating_neuron] = 0.01

    def disconnect_neurons(self, originating_neuron, destination_neuron):
        '''
        Disconnect between 2 connected neurons.
        
        @param originating_neuron: name of neuron to disconnect from
        @type originating_neuron: string
        @param destination_neuron: name of neuron to disconnect to
        @type destination_neuron: string
        '''
        originating_neuron = str(originating_neuron)
        destination_neuron = str(destination_neuron)
        if originating_neuron not in self.synapses:
            raise AttributeError('Originating neuron name, %s, is not \
            found - this neuron has not been created. Disconnection can \
            only take place between 2 existing and connected neurons' % 
            originating_neuron)
        elif destination_neuron not in self.synapses:
            raise AttributeError('Destination neuron name, %s, is not \
            found - this neuron has not been created. Disconnection can \
            only take place between 2 existing and connected neurons' % 
            destination_neuron)
        elif originating_neuron not in self.synapses[destination_neuron]:
            raise AttributeError('No existing connection/synapse exist \
            between %s and %s. Disconnection can only take place between \
            2 existing and connected neurons' % (originating_neuron, 
                                                 destination_neuron))
        else:
            del self.synapses[destination_neuron][originating_neuron]

    def set_activation_sequence(self, activation_sequence):
        '''
        Set neuron activation sequence or replace current neuron 
        activation sequence.
        
        @param activation_sequence: list of list of activation sequence
        '''
        if type(activation_sequence) != type([]):
            raise AttributeError('Parameter, activation_sequence, must \
            be a list but %s type given' % str(type(activation_sequence)))
        else:
            self.activation_sequence = activation_sequence
            
    def add_neuron_to_activation_sequence(self, neuron_name, position):
        '''
        Add neuron to activation sequence.
        
        @param neuron_name: name of neuron to add
        @type neuron_name: string
        @param position: position to add neuron, where position > 0
        @type position: integer
        '''
        position = int(position)
        neuron_name = str(neuron_name)
        if neuron_name not in self.synapses:
            raise AttributeError('Neuron %s, is not found - it is only \
            possible to add an existing neuron to activation_sequence.' 
            % neuron_name)
        else:
            if position > (len(self.activation_sequence)):
                self.activation_sequence.append([neuron_name])
            else:
                self.activation_sequence[position-1].append(neuron_name)
    
    def remove_neuron_from_activation_sequence(self, neuron_name, 
                                               position='all'):
        '''
        Remove neuron from activation sequence.
        
        @param neuron_name: name of neuron to remove
        @type neuron_name: string
        @param position: position to add neuron, where position > 0 
        (integer) or 'all' (string). If position = 'all', this method will 
        remove neuron from the entire activation sequence
        '''
        neuron_name = str(neuron_name)
        if position == 'all':
            for i in range(len(self.activation_sequence)):
                self.activation_sequence[i] = \
                    [neuron for neuron in self.activation_sequence[i] 
                     if neuron != neuron_name]
        else:
            position = int(position)
            try: self.activation_sequence[position] = \
                    [neuron for neuron in self.activation_sequence[i] 
                     if neuron != neuron_name]
            except IndexError: pass
        self.activation_sequence = \
            [sequence for sequence in self.activation_sequence 
             if len(sequence) > 0]
        
    def add_neuron(self, neuron=None):
        '''
        Add a neuron into the brain.
        
        @param neuron: the neuron to be added. If None, then a generic 
        neuron will be created and added. Default = None.
        @type neuron: Neuron object
        '''
        if neuron == None: neuron = Neuron()
        self.neuron_pool[neuron.name] = neuron
        self.activations[neuron.name] = 0.0
        self.synapses[neuron.name] = {}
        
    def remove_neuron(self, neuron_name):
        '''
        Removing a neuron from the brain.
        
        @param neuron_name: name of neuron to remove
        @type neuron_name: string
        '''
        neuron_name = str(neuron_name)
        if neuron_name not in self.synapses:
            raise AttributeError('Neuron %s, is not found - it is only \
            possible to remove an existing neuron.' % neuron_name)
        else:
            # remove neuron from neuron_pool
            neuron = copy.deepcopy(self.neuron_pool[neuron_name])
            del self.neuron_pool[neuron_name]
            # remove synapses to the neuron
            del self.synapses[neuron_name]
            # remove all synapses from the neuron
            for name in self.synapses.keys():
                try: 
                    del self.synapses[name][neuron_name]
                except KeyError: pass
            # remove neuron from activation_sequence
            self.remove_neuron_from_activation_sequence(neuron_name, 'all')
            return neuron
    
    def empty_brain(self):
        '''
        Empty/clear the entire brain of all neurons, connections and 
        states.
        '''
        self.activations.clear()
        self.neuron_pool.clear()
        self.synapses.clear()
        self.activation_sequence = []
