"""!
COPADS (Collection of Python Algorithms and Data Structures).

The main aim of COPADS is to develop a compilation of of Python data
structures and its algorithms, making it almost a purely developmental
project. Personally, I look at this as a re-usable collection of tools
that I can use in other projects. Therefore, this project is 
essentially "needs-driven", except a core subset of data structures 
and algorithms.

This project originated from 3 threads of thought. Firstly, while 
browsing through Mehta and Sahni's Handbook of Data Structures and 
Applications, I thought there might be utility to have a number of the 
listed data structures implemented in Python. Given my interest in 
biological data management, having a good set of data structures is 
always handy. The 2nd thread of thought came from Numerical Recipes. 
Again, I thought these algorithms will be handy to have and had 
started to translate some of them into Python during some overly 
energetic days. Finally, Python Cookbook had undergone 2 editions by 
2008 and ActiveState had provided an online platform for Python 
Recipes which I found to be useful and can see how some of these 
recipes can be merged. Thus, COPADS is borned.

Project website: https://github.com/mauriceling/copads

License: Unless specified otherwise, all parts of this package, except
those adapted, are covered under Python Software Foundation License
version 2.
"""
from datetime import datetime

__version__ = '1.0.0'

__author__ = 'Maurice H.T. Ling <mauriceling@acm.org> on behalf of all developers'

__copyright__ = '(c) 2007-%s, Maurice H.T. Ling.' % (datetime.now().year)

# Constants
from .constants import * 

# Data Structures
from .dsDeque import Deque
from .dsHashTable import HashTable
from .dsOrderedList import OrderedList
from .dsQueue import Queue
from .dsStack import Stack
from .dsUnorderedList import UnorderedList

# Operational classes
from .lindenmayer import Lindenmayer
from .pnet import PNet
from .randomize import MersenneTwister
from .randomize import LCG
from .randomize import CLCG
from .statisticsdistribution import BetaDistribution
from .statisticsdistribution import BinomialDistribution
from .statisticsdistribution import CauchyDistribution
from .statisticsdistribution import ChiSquareDistribution
from .statisticsdistribution import CosineDistribution
from .statisticsdistribution import ErlangDistribution
from .statisticsdistribution import ExponentialDistribution
from .statisticsdistribution import FDistribution
from .statisticsdistribution import FrechetDistribution
from .statisticsdistribution import FurryDistribution
from .statisticsdistribution import GammaDistribution
from .statisticsdistribution import GeometricDistribution
from .statisticsdistribution import HypergeometricDistribution
from .statisticsdistribution import LogarithmicDistribution
from .statisticsdistribution import NormalDistribution
from .statisticsdistribution import PoissonDistribution
from .statisticsdistribution import SemicircularDistribution
from .statisticsdistribution import TDistribution
from .statisticsdistribution import TriangularDistribution
from .statisticsdistribution import UniformDistribution
from .statisticsdistribution import WeiBullDistribution

# Operational functions
from . import hypothesis
from . import nrpy
from . import objectdistance
from . import ode

# Type-casting functions

