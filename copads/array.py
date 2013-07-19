"""
Array Data Structures and Algorithms.

Copyright (c) Maurice H.T. Ling <mauriceling@acm.org>

Date created: 19th March 2008
"""

from copadsexceptions import ArrayError

class ParallelArray(object):

    
    """
    Parallel Array is an array whereby each data list in the array is of the
    same size.
    Ref: http://en.wikipedia.org/wiki/Parallel_array
    """

    def __init__(self, fields = None):
        """Constructor. Able to initiate the array with a list of fields names        
        @param fields: list of field names to initiate. Default = None"""
        self.data = {}
        self.fields = []
        if fields:
            self.initFields(kwargs['fields'])  
          
    def initFields(self, fields):
        """Initiates a list of fields into the array.
        
        @param fields: list of field names to initiate."""
        if type(fields) <> type([]):
            raise ArrayError('field parameter must be a list, ' + \
                str(type(fields)) + ' given.')
        for field in fields: self.addField(field)  
              
    def addField(self, field):
        """Method to add a new field into the array. Raises ArrayError if 
        attempt to add an existing field.
        
        @param field: name of field
        @type field: string"""
        if field in self.data:
            raise ArrayError(str(field) + ' existed.')
        if type(field) <> type('string'):
            raise ArrayError('field must be a string')
        if len(self.fields) == 0: self.initFields(list(field))
        else:
            ddata = [None for x in range(len(self.data[self.fields[0]]))]
            self.data[field] = ddata
            self.fields.append(field)
            self.field_len = len(self.fields)
            
    def removeField(self, field):
        """Removes a field, together with its data, from the array.
        
        @param field: name of field
        @type field: string"""
        try:
            self.data.pop(field)
            self.fields.remove(field)
            self.field_len = len(self.fields)
        except KeyError: pass
        
    def changeField(self, oldname, newname):
        """Change a field name.
        
        @param oldname: existing name of field
        @type oldname: string
        @param newname: new name to change to. A new field by this name will
            be created if 'oldname' is not found
        @type newname: string"""
        if self.data.has_key(newname):
            raise ArrayError(str(newname) + ' already exist in array.')
        if self.data.has_key(oldname):
            temp = self.data[oldname]
            self.removeField(oldname)
            self.data[newname] = temp
        else: self.addField(newname)
        
    def addData(self, fields, data):
        """Add data into the array
        
        @param fields: ordered list of fields
        @param data: ordered list of data to add"""
        if len(fields) <> len(data):
            raise ArrayError('Field size and data length are different')
        for x in fields:
            if not self.data.has_key(x):
                raise ArrayError(str(x) + ' field not found')
        for i in range(len(fields)):
            self.data[fields[i]].append(data[i])
    
