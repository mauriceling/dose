"""
Ring Data Structures and Algorithms.

Copyright (c) Maurice H.T. Ling <mauriceling@acm.org>

Date created: 19th March 2008
"""

class RingList:
    """
    The RingList is a class implementing a circular list. The ring have a 
    fixed size and when it is full and you append a new element, the first 
    one will be deleted. The class lets you access to the data like a python 
    list or like a string.

    Adapted from: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/435902 
    Original author: Flavio Catalani
    """
    def __init__(self, length):
        """
        Initializes an empty RingList of maximum given length as given in 
        length parameter"""
        self.__data__ = []
        self.__full__ = 0
        self.__max__ = length
        self.__cur__ = 0

    def append(self, x):
        """Append parameter x to the data structure."""
        if self.__full__ == 1:
            for i in range (0, self.__cur__ - 1):
                self.__data__[i] = self.__data__[i + 1]
            self.__data__[self.__cur__ - 1] = x
        else:
            self.__data__.append(x)
            self.__cur__ += 1
            if self.__cur__ == self.__max__:
                self.__full__ = 1

    def get(self):
        """Retrieves the data."""
        return self.__data__

    def remove(self):
        """Removes the last element of the ring."""
        if (self.__cur__ > 0):
            del self.__data__[self.__cur__ - 1]
            self.__cur__ -= 1

    def size(self):
        """Returns the current size of the ring."""
        return self.__cur__

    def maxSize(self):
        """Returns the maximum allowed size of the ring."""
        return self.__max__

    def __str__(self):
        """Returns the ring as a string."""
        return ''.join(self.__data__) 
        
