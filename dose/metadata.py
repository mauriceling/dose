'''
Digital Organism Simulation Environment (DOSE) Metadata

Date created: 14th February 2014
'''

pypi_name = 'digital organism simulation environment'
description = 'Digital Organism Simulation Environment (DOSE)'
version = '1.0.5'
maintainer = 'Maurice HT Ling'
email = 'mauriceling@acm.org'
download_url = 'https://github.com/mauriceling/dose/releases'
project_start_year = '2010'
project_website = 'https://github.com/mauriceling/dose'
documentation_website = 'https://github.com/mauriceling/dose/wiki'
short_license = 'GNU General Public License version 3'
long_license = '''
Unless otherwise specified, dose.copads package will be licensed 
under Python Software Foundation License version 2; all other files will 
be licensed GNU General Public License version 3.'''
platforms = ['Operating System :: OS Independent']
trove_classifiers = \
    ['Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2 :: Only',
    'Topic :: Education',
    'Topic :: Scientific/Engineering :: Artificial Life',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'Topic :: Software Development :: Libraries :: Python Modules'
    ]

from datetime import datetime
copyright_year = '-'.join([project_start_year, 
                           str(datetime.now().year)])
                           
long_description = '''%s

Life is fascinating and deeply intriguing. Despite so, life forms on Earth 
or carbon-based life forms as a group is just one form, one possible sample 
of possibly a whole magnitude of life. Even then, there are many aspects of 
life that cannot be deciphered even by examining current life forms; for 
example, how did chemical reactions organize themselves into biochemical 
pathways? How did life start? How is intelligence formed?

To answer such questions, we will have to restart our evolutionary time to 
the very beginning - clearly an impossibly gargantuan task. At the same 
time, studying biological/carbon-based life forms is expensive, time 
consuming and destructive. As a molecular biologist, there is no way I can 
examine the entire genome of even a bacteria in an inanimate state, then 
somehow allow it to continue living as if time had just stopped while I 
am examining it.

However, if I can simulate a bacteria or any life form in a computer, 
then I can make a digital copy of the bacterium, pull it apart to study it 
while the original bacterium continues "living" in my virtual world without 
even knowing that it had been duplicated. Many biologists thought of virtual 
life forms as a new way to learn about life itself. Studying of virtual life 
forms is known as Artificial Life and I term "virtual life forms" as 
"digital organisms". There are several advantages in experimenting using 
digital organisms. Firstly, generation time can be much faster compared to 
most biological life. Secondly, it is usually cheaper to examine computer 
simulations than working on actual biological life. Perhaps the most 
important advantage of looking at life from this perspective is that by 
recreating life in a different medium, we are not limited to our own system 
of carbon-based life; hence, studying life as what-it-could-be.

Digital Organisms Simulation Environment (DOSE) is essentially a virtual 
world simulator for studying digital organisms. I will argue that digital 
organisms are considered living organisms (Koh and Ling, 2013). Despite so, 
being a molecular biologist by training, I have a hard time mapping 
components of digital organisms into biological life whenever such 
components are too abstract.

Hence, I decided to design an artificial life / digital organism simulator 
that bears resemblance to biological life and ecology. These are the 
foundation papers:

1. Lim, JZR, Aw, ZQ, Goh, DJW, How, JA, Low, SXZ, Loo, BZL, Ling, MHT. 2010. 
A genetic algorithm framework grounded in biology. The Python Papers Source 
Codes 2: 6. 

This manuscript describes the implementation of a GA framework that uses 
biological hierarchy - from chromosomes to organisms to population.

2. Ling, MHT. 2012. An Artificial Life Simulation Library Based on Genetic 
Algorithm, 3-Character Genetic Code and Biological Hierarchy. The Python 
Papers 7: 5. 

Genetic algorithm (GA) is inspired by biological evolution of genetic 
organisms by optimizing the genotypic combinations encoded within each 
individual with the help of evolutionary operators, suggesting that GA 
may be a suitable model for studying real-life evolutionary processes. 
This paper describes the design of a Python library for artificial life 
simulation, Digital Organism Simulation Environment (DOSE), based on GA 
and biological hierarchy starting from genetic sequence to population. 
A 3-character instruction set that does not take any operand is 
introduced as genetic code for digital organism. This mimics the 3-
nucleotide codon structure in naturally occurring DNA. In addition, 
the context of a 3-dimensional world composing of ecological cells is 
introduced to simulate a physical ecosystem.

- Ling, MHT. 2012. Ragaraja 1.0: The Genome Interpreter of Digital 
Organism Simulation Environment (DOSE). The Python Papers Source Codes 
4: 2. 

This manuscript describes the implementation and test of Ragaraja 
instruction set version 1.0, which is the core genomic interpreter of 
DOSE.

From this foundation, the complete suite of Digital Organisms Simulation 
Environment (DOSE) can be build.

Project website: U{%s}

Documentation can be found at %s

License: %s

Copyright %s, Maurice HT Ling (on behalf of all authors).
''' % (description,
       project_website, 
       documentation_website, 
       long_license, 
       copyright_year)
