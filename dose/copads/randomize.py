'''!
A collection of (pseudo)-random number generators

Date created: 18th February 2016

Licence: Python Software Foundation License version 2
'''
import sys
import random

try:
    randgen = random.SystemRandom()
except:
    randgen = random


class Randomizer(object):
    '''!
    Abstract class for all random number generators (RNG).
    '''
    def __init__(self, seed=None):
        '''!
        Constructor method.

        @param seed integer: seed to start the RNG. Default = None,
        a random seed will be generated.
        '''
        if seed == None:
            self.seed = int(randgen.random()*1000000)
        else:
            self.seed = int(seed)

    def _random(self):
        '''!
        Method to hold algorithm to generate a random integer. This 
        method will be called by other methods.
        
        @return a random generated integer.
        '''
        raise NotImplementedError
        
    def randrange(self, start=0, stop=2147483647):
        '''!
        Method to generate a random integer between start and stop
        (start < random_number <= stop).

        @param start integer: lower boundary of random integer (not 
        includsive) to generate. Default = 0.
        @param stop integer: upper boundary of random integer (
        inclusive) to generate. Default = 2147483647.
        '''
        x = self._random() + int(start)
        return int(x % int(stop))

    def randint(self):
        '''!
        Method to generate a random integer between 0 (not inclusive) 
        and the maximum integer allowable by system (inclusive)
        '''
        return self.randrange()
        
    def random(self):
        '''!
        Method to generate a random float between zero (not inclusive)
        and one (inclusive) (0 < random_float <= 1).
        '''
        x = float(self._random()) / float(self._random())
        return abs(x) % 1

    def choice(self, sequence):
        '''!
        Method to randomly select an element from a sequence.

        @param sequence list: sequence to select from.
        @return an element in sequence.
        '''
        index = self.randrange(0, len(sequence)-1)
        return seq[index]

    
class MersenneTwister(Randomizer):
    '''!
    32-bit Mersenne twister algorithm (MT19937).
    
    Adapted from https://en.wikipedia.org/wiki/Mersenne_Twister
    
    Reference: Matsumoto, M., Nishimura, T. (1998). Mersenne twister:
    a 623-dimensionally equidistributed uniform pseudo-random number
    generator. ACM Transactions on Modeling and Computer Simulation 8
    (1): 3-30. doi:10.1145/272991.272995
    '''
    def __init__(self, seed=None):
        '''!
        Constructor method.

        @param seed integer: seed to start the RNG. Default = None,
        a random seed will be generated.
        '''
        if seed == None:
            self.seed = int(randgen.random()*1000000)
        else:
            self.seed = int(seed)
        self.index = 624
        self.block = [0] * 624
        self.block[0] = int(self.seed)
        for i in range(1, 624):
            t = self.block[i-1] ^ (self.block[i-1] >> 30)
            self.block[i] = self._int32(1812433253 * t + i)

    def _int32(self, x):
        '''!
        Private method to get the 32 least significant bits.
        '''
        return int(0xFFFFFFFF & x)
    
    def random(self):
        '''!
        Method to generate a random integer.
        
        @return a random generated integer.
        '''
        if self.index >= 624: self._twist()
        y = self.block[self.index]
        # Right s+hift by 11 bits
        y = y ^ (y >> 11)
        # Shift y left by 7 and take the bitwise and of 2636928640
        y = y ^ ((y << 7) & 2636928640)
        # Shift y left by 15 and take the bitwise and of y and 4022730752
        y = y ^ ((y << 15) & 4022730752)
        # Right shift by 18 bits
        y = y ^ (y >> 18)
        self.index = self.index + 1
        return self._int32(y)
    
    def _twist(self):
        '''!
        Private method to generate twist.
        '''
        for i in range(624):
            # Get the most significant bit and add it to the less significant
            # bits of the next number
            t = self.block[(i+1) % 624] & 0x7fffffff
            y = self._int32((self.block[i] & 0x80000000) + t)
            self.block[i] = self.block[(i+397) % 624] ^ (y >> 1)
            if y % 2 != 0:
                self.block[i] = self.block[i] ^ 0x9908b0df
        self.index = 0


class LCG(Randomizer):
    '''!
    A set of linear congruential generators (LCG) and LCG-based generators to generate a sequence of pseudorandom numbers. LCG has the general equation of
    
    x(n+1) = [multiplier * x(n) + increment] % modulus
        
    where
    
        1. increment (also known as offset) and modulus are co-primes
        2. (multiplier - 1) is divisible by all prime factors of modulus
        3. (multiplier - 1) is divisible by 4 if modulus is divisible by 4
        
    Depending on the parameters, different LCGs exist. If increment is 
    zero, the LCG is known as multiplicative congruential generator (
    MCG). If increment is not zero, the LCG is known as mixed 
    congruential generator.
    '''
    def __init__(self, seed=None, generator='mmix'):
        '''!
        Constructor method.

        @param seed integer: seed to start the RNG. Default = None,
        a random seed will be generated.
        @param generator string: type of generator. Default = 'mmix'. Allowable types are:
            - ansic: ANSI C (32-bit)
            - borlandc: Borland C/C++ (32-bit)
            - crc: CRC vector machine (48-bit)
            - java: Java.utils.Random (48-bit)
            - lehmer: Lehmer RNG (also known as MINSTD or Park-Miller RNG) (32-bit)
            - lehmer2: Lehmer RNG (also known as MINSTD2)
            - lehmer3: Lehmer RNG (also known as MINSTD3)
            - mmix: MMIX by Donald Knuth (64-bit)
            - newlib: NewLib (http://www.sourceware.org/newlib/) (64-bit)
            - nag: Numerical Algorithms Group (64-bit)
            - nr: defined in Numerical Recipes (32-bit)
            - pascal: Borland Delphi/Visual Pascal (32-bit)
            - vb6: Microsoft Visual Basic 6 and below (24-bit)
            - visualc: Microsoft Visual C/C++ (32-bit)
        '''
        if seed == None:
            self.seed = int(randgen.random()*1000000)
        else:
            self.seed = int(seed)
        if generator == 'nr':
            self.multiplier = 1664525
            self.increment = 1013904223
            self.modulus = 2**32
        elif generator == 'borlandc':
            self.multiplier = 22695477
            self.increment = 1
            self.modulus = 2**32
        elif generator == 'pascal':
            self.multiplier = 134775813
            self.increment = 1
            self.modulus = 2**32
        elif generator == 'visualc':
            self.multiplier = 214013	
            self.increment = 2531011
            self.modulus = 2**32
        elif generator == 'vb6':
            self.multiplier = 1140671485	
            self.increment = 12820163
            self.modulus = 2**24
        elif generator == 'nag':
            self.multiplier = 13**13
            self.increment = 0
            self.modulus = 2**59
        elif generator == 'newlib':
            self.multiplier = 6364136223846793005	
            self.increment = 1
            self.modulus = 2**64
        elif generator == 'java':
            self.multiplier = 25214903917
            self.increment = 11
            self.modulus = 2**48
        elif generator == 'lehmer':
            self.multiplier = 16807
            self.increment = 0
            self.modulus = 2**31 - 1
        elif generator == 'lehmer2':
            self.multiplier = 48271
            self.increment = 0
            self.modulus = 2**31 - 1
        elif generator == 'lehmer3':
            self.multiplier = 69621
            self.increment = 0
            self.modulus = 2**31 - 1
        elif generator == 'ansic':
            self.multiplier = 1103515245
            self.increment = 12345
            self.modulus = 2**31
        elif generator == 'cdc':
            self.multiplier = 5**15
            self.increment = 0
            self.modulus = 2**47
        else:                               # generator == 'mmix'
            self.multiplier = 6364136223846793005	
            self.increment = 1442695040888963407
            self.modulus = 2**64

    def random(self):
        '''!
        Method to generate a random integer using the following 
        equation where 
        x(n+1) is a newly generated integer
        
        x(n+1) = [multiplier * x(n) + increment] % modulus
        
        @return a random generated integer.
        '''
        t = (self.multiplier * self.seed) + self.increment
        self.seed = t % self.modulus
        return self.seed


class CLCG(Randomizer):
    '''!
    Combined linear congruential generator (CLCG), made by combining 2 
    linear congruential generators.
    '''
    def __init__(self, seedA=None, generatorA='mmix',
                 seedB=None, generatorB='mmix'):
        '''!
        Constructor method.

        @param seedA integer: seed to start the the first LCG. Default 
        = None, a random seed will be generated.
        @param generatorA string: type of generator for first LCG. 
        Default = 'mmix'. Allowable types are the same as LCG.
        @param seedB integer: seed to start the the second LCG. 
        Default = None, a random seed will be generated.
        @param generatorB string: type of generator for second LCG. 
        Default = 'mmix'. Allowable types are the same as LCG.
        '''
        self.LCG_A = LCG(seedA, generatorA)
        self.LCG_B = LCG(seedB, generatorB)
        self.modulus = max(self.LCG_A.modulus, self.LCG_B.modulus)
        
    def random(self):
        '''!
        Method to generate a random integer using the following 
        equation where s is a newly generated integer
        
        x(n+1) = [multiplierX * x(n) + incrementX] % modulusX
        
        y(n+1) = [multiplierY * y(n) + incrementY] % modulusY
        
        s = [x(n+1) + y(n+1)] % max(modulusX, modulusY)
        
        @return a random generated integer.
        '''
        rA = self.LCG_A.random()
        rB = self.LCG_B.random()
        t = (rA + rB) % self.modulus
        return t * self.modulus
        

