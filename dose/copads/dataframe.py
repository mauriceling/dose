'''
A generic dataframe to hold data and analysis
Date created: 24th September 2012
Licence: Python Software Foundation License version 2
'''
from copadsexceptions import FunctionParameterValueError

class dataframe(object):
    '''
    A data frame is an encapsulation of one or more data series and its 
    associated analyses.
    '''

    data = {}
    analyses = {}
    data_length = 0
    frame_name = ''
    
    def __init__(self, name=''):
        '''
        Constructor. Initialize data frame with a name.
        
        @param name: Name of this data frame
        @type name: string
        '''
        self.frame_name = str(name)
    
    def addSeries(self, name, data=[]):
        '''
        Add a data series (vector/column) to the frame.
        
        @param name: Name of data series
        @type name: string
        @param data: Data to be added
        @type data: list
        '''
        self.data[name] = data
        if self.data_length < len(data):
            self.data_length = len(data)
        
    def changeDataType(self, name, type='float'):
        '''
        Change the data type for a data series
        
        @param name: Name of data series
        @type name: string
        @param type: Type of data to cast data series into. Allowable = {float |
        integer | string | long}. Default = float
        '''
        if type == 'float':
            self.data[name] = [float(x) for x in self.data[name]]
        elif type == 'integer':
            self.data[name] = [int(x) for x in self.data[name]]
        elif type == 'string':
            self.data[name] = [str(x) for x in self.data[name]]
        elif type == 'long':
            self.data[name] = [long(x) for x in self.data[name]]
        else:
            raise FunctionParameterValueError('Unknown data type: ' + str(type))
            
    def getSeries(self, name):
        '''
        Get values of a data series.
        
        @param name: Name of data series
        @type name: string
        @return: List of data
        '''
        if self.has_series(name): 
            return self.data[name]
        else:
            raise FunctionParameterValueError('Unknown data series: ' + str(name))
        
    def has_series(self, name):
        '''
        Check whether data frame has a certain data series (by name).
        
        @param name: Name of data series
        @type name: string
        @return: True, if the data series is present; False, if the data series
        is absent
        '''
        if self.data.has_key(name): 
            return True
        else: 
            return False
        
    def changeDatum(self, name, observation, newvalue):
        '''
        Change the value of a datum in a data series.
        
        @param name: Name of data series
        @type name: string
        @param observation: Observation number to change (starting count = 1)
        @type observation: integer
        @param newvalue: new value for the observation
        '''
        observation = int(observation)
        if not self.has_series(name): 
            raise FunctionParameterValueError('Unknown data series: ' + str(name))
        if observation > len(self.data[name]):
            raise FunctionParameterValueError('Unknown observation: ' + \
                                              str(observation))
        self.data[name][observation-1] = newvalue
       
    def getObservation(self, observation):
        '''
        Get values of an observation
        
        @param observation: Observation number to change (starting count = 1)
        @type observation: integer
        @return: Dictionary of data
        '''
        temp = {}
        for key in self.data.keys():
            try:
                temp[key] = self.data[key][observation-1]
            except IndexError:
                temp[key] = None
        return temp