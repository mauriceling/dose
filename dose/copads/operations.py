"""
Mathematical Operation Routines.

Copyright (c) Maurice H.T. Ling <mauriceling@acm.org>

Date created: 19th March 2008
"""

import math
import itertools
import random
import constants

class Modulus2:
    """
    Class for Modulus 2 arithmetics
    
    @status: Tested methods
    @since: version 0.1
    """
    def __init__(self, input = 0):
        self.datum = input

    def __add__(self, other):
        if self.datum == 0 and other == 0: return 0
        if self.datum == 1 and other == 0: return 1
        if self.datum == 0 and other == 1: return 1
        if self.datum == 1 and other == 1: return 0

    def __mul__(self, other):
        if self.datum == 0 and other == 0: return 0
        if self.datum == 1 and other == 0: return 0
        if self.datum == 0 and other == 1: return 0
        if self.datum == 1 and other == 1: return 1

    def __str__(self): return str(self.datum)
        

class Boolean:
    """
    Class for Boolean arithmetics
    
    @status: Tested methods
    @since: version 0.1
    """
    def __init__(self, input = 0):
        self.datum = input

    def __add__(self, other):
        if self.datum == 0 and other == 0: return 0
        if self.datum == 1 and other == 0: return 1
        if self.datum == 0 and other == 1: return 1
        if self.datum == 1 and other == 1: return 1

    def __mul__(self, other):
        if self.datum == 0 and other == 0: return 0
        if self.datum == 1 and other == 0: return 0
        if self.datum == 0 and other == 1: return 0
        if self.datum == 1 and other == 1: return 1

    def __str__(self): return str(self.datum)
   
def asdict(l):
    """asdict(l) -> dictionary

    Return a dictionary where the keys are the items in the list, with
    arbitrary values.  This is useful for quick testing of membership.
    Adapted from BioPython.
    """
    return count(l)

def items(l):
    """items(l) -> list of items

    Generate a list of one of each item in l.  The items are returned
    in arbitrary order.
    Adapted from BioPython.
    """
    try:
        return list(asdict(l).keys())
    except TypeError, x:
        if str(x).find("unhashable") == -1:
            raise
    # asdict failed because l is unhashable.  Back up to a naive
    # implementation.
    l = l[:]
    l.sort()
    i = 0
    while i < len(l)-1:
        if l[i] == l[i+1]:
            del l[i]
        else:
            i += 1
    return l

def count(items):
    """count(items) -> dict of counts of each item

    Count the number of times each item appears in a list of data.
    Adapted from BioPython.
    """
    c = {}
    for i in items:
        c[i] = c.get(i, 0) + 1
    return c

def contents(items):
    """contents(items) -> dict of item:percentage

    Summarize the contents of the list in terms of the percentages of each
    item.  For example, if an item appears 3 times in a list with 10 items,
    it is in 0.3 of the list.
    Adapted from BioPython.
    """
    counts = count(items)
    l = float(len(items))
    contents = {}
    for i, c in list(counts.items()):
        contents[i] = c / l
    return contents

def itemindex(l):
    """itemindex(l) -> dict of item : index of item

    Make an index of the items in the list.  The dictionary contains
    the items in the list as the keys, and the index of the first
    occurrence of the item as the value.
    Adapted from BioPython.
    """
    dict = {}
    for i in range(len(l)):
        if not dict.has_key(l[i]):
            dict[l[i]] = i
    return dict

def indexesof(l, fn, opposite=0):
    """indexesof(l, fn) -> list of indexes

    Return a list of indexes i where fn(l[i]) is true.
    Adapted from BioPython.
    """
    indexes = []
    for i in range(len(l)):
        f = fn(l[i])
        if (not opposite and f) or (opposite and not f):
            indexes.append(i)
    return indexes

def take(l, indexes):
    """take(l, indexes) -> list of just the indexes from l
    Adapted from BioPython."""
    items = []
    for i in indexes:
        items.append(l[i])
    return items

def take_byfn(l, fn, opposite=0):
    """Adapted from BioPython."""
    indexes = indexesof(l, fn, opposite=opposite)
    return take(l, indexes)
 
def fcmp(x, y, precision):
    """fcmp(x, y, precision) -> -1, 0, or 1"""
    if math.fabs(x-y) < precision:
        return 0
    elif x < y:
        return -1
    return 1

def intd(x, digits_after_decimal=0):
    """intd(x[, digits_after_decimal]) -> int x, rounded

    Represent a floating point number with some digits after the
    decimal point as an integer.  This is useful when floating point
    comparisons are failing due to precision problems.  e.g.
    intd(5.35, 1) -> 54.
    Adapted from BioPython.
    """
    precision = 10.**digits_after_decimal
    if x >= 0:
        x = int(x * precision + 0.5)
    else:
        x = int(x * precision - 0.5)
    return x

def safe_log(n, zero=None, neg=None):
    """safe_log(n, zero=None, neg=None) -> log(n)

    Calculate the log of n.  If n is 0, returns the value of zero.  If n is
    negative, returns the value of neg.
    Adapted from BioPython.
    """
    if n < 0:
        return neg
    elif n < 1E-100:
        return zero
    return math.log(n)

LOG2 = math.log(2)

def safe_log2(n, zero=None, neg=None):
    """safe_log2(n, zero=None, neg=None) -> log(n)

    Calculate the log base 2 of n.  If n is 0, returns the value of
    zero.  If n is negative, returns the value of neg.
    Adapted from BioPython.
    """
    l = safe_log(n, zero=zero, neg=neg)
    if l is None:
        return l
    return l/LOG2

def safe_exp(n, under=None, over=None):
    """safe_exp(n, under=None, over=None) -> e**n

    Guaranteed not to overflow.  Instead of overflowing, it returns
    the values of 'under' for underflows or 'over' for overflows.
    Adapted from BioPython.
    """
    try:
        return math.exp(n)
    except OverflowError:
        if n < 0:
            return under
        return over
    raise "How did I get here?"

def factorial(n):
    """Calculates and return n! where n is an integer, or will be casted
    as an integer."""
    n = int(n)
    if n == 0: return 1
    else: return n * factorial(n - 1)
    
def fibonacci(n):
    """Calculates and return the sum of the first n-th Fibonacci number"""
    n = int(n)
    if n < 1: return 0
    if n == 1: return 1
    return fibonacci(n - 1) + fibonacci(n - 2)
    
def permutation(items, n=None):
    """
    Generates permutation of n-elements from the list of input items. 
    For example, if n = 2, this function will generate permutations
    of 2-elements.
    
    Adapted from Raymond Hettinger's comment to 
    http://code.activestate.com/recipes/474124/"""
    if n is None:
        n = len(items)
    for i in range(len(items)):
        v = items[i:i+1]
        if n == 1:
            yield v
        else:
            rest = items[:i] + items[i+1:]
            for p in permutation(rest, n-1):
                yield v + p

def combination(items, n=None):
    """
    Generates combination of n-elements from the list of input items. 
    For example, if n = 2, this function will generate combinations
    of 2-elements.
    
    Adapted from Raymond Hettinger's comment to 
    http://code.activestate.com/recipes/474124/"""
    if n is None:
        n = len(items)
    for i in range(len(items)):
        v = items[i:i+1]
        if n == 1:
            yield v
        else:
            rest = items[i+1:]
            for c in combination(rest, n-1):
                yield v + c
          
def sample_wr(population, k):
    """
    Chooses k random elements (with replacement) from a population.
    Adapted from Raymond Hettinger's comment to 
    http://code.activestate.com/recipes/273085/
    
    @since: version 0.2
    """
    n = len(population)
    _random, _int = random.random, int  # speed hack
    selection = [_int(_random() * n) for i in itertools.repeat(None, k)]
    return [population[index] for index in selection]

def sample(population, k):
    """
    Chooses k random elements (without replacement) from a population.
    
    @since: version 0.2
    """
    _random, _int = random.random, int
    if len(population) < k: return False
    t = range(k)
    for i in range(k):
        t[i] = population[_int(_random() * len(population))]
        #print population
        #print t[i]
        population.remove(t[i])
    return t

def summation(x):
    """
    Sum of all the elements of x"""
    x = list(x)
    sum = 0.0
    for i in range(len(x)): sum = sum + x[i]
    return sum

def product(x):
    """
    Product of all the elements of x, also known as series product"""
    x = list(x)
    sum = 1.0
    for i in range(len(x)): sum = sum * x[i]
    return sum
