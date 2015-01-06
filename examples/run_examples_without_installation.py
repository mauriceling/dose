'''
This file contains inserts the path for DOSE into system path to
allow for any examples importing this file to execute without 
needing DOSE to be installed into into Python site-packages.
'''
import sys
import os

cwd = os.getcwd().split(os.sep)
#cwd[-1] = 'dose'
cwd = os.sep.join(cwd[:-1])

sys.path.append(cwd)

import dose
