"""
Node Classes for Tree Data Structures.

Copyright (c) Maurice H.T. Ling <mauriceling@acm.org>

Date created: 19th March 2008
"""

# RBTree colour code
BLACK = 0
RED = 1

class RBNode(object):

    def __init__(self, key = None, value = None, color = RED):
        self.left = self.right = self.parent = None
        self.color = color
        self.key = key
        self.value = value
        self.nonzero = 1
        self.count = 1

    def __str__(self):
        return repr(self.key) + ': ' + repr(self.value)

    def __nonzero__(self):
        return self.nonzero

    def __len__(self):
        """imitate sequence"""
        return 2

    def __getitem__(self, index):
        """imitate sequence"""
        if index==0:
            return self.key
        if index==1:
            return self.value
        raise IndexError('only key and value as sequence')
    
class BinaryNode:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data 
        
class ThreeNode:
    def __init__(self, data):
        self.left = None
        self.centre = None
        self.right = None
        self.data = data
        
class FourNode:
    def __init__(self, data):
        self.left = None
        self.centre = None
        self.centre2 = None
        self.right = None
        self.data = data