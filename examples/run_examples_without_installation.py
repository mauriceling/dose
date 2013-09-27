import sys
import os

cwd = os.getcwd().split(os.sep)
cwd[-1] = 'dose'
cwd = os.sep.join(cwd)

sys.path.append(cwd)
