'''
Example 19e: Using Lindenmayer system to draw a Tree
'''
# needed to run this example without prior
# installation of DOSE into Python site-packages
try: 
	import run_examples_without_installation
except ImportError: pass

# Example codes starts from here
import dose, random

axiom = 'F'
rules = [['F', '0FFL[1LFRFRF]R[2RFLFLF]']]
start_position = (0, -200)
iterations = 5
turtle_file = '19_lindenmayer_tree_turtle.py'
image_file = '19_lindenmayer_tree_turtle.svg'
mapping = {'set_angle': 22,
           'random_angle': 0,
           'set_distance': 5,
           'random_distance': 0,
           'set_heading': 90,
           'background_colour': 'ivory',
           'F': 'forward',
           'R': 'right',
           'L': 'left',
           '[': 'push',
           ']': 'pop',
           '0': 'brown',
           '1': 'dark green',
           '2': 'forest green'
           }
           
lindenmayer = dose.lindenmayer(1)
lindenmayer.add_rules(rules)
lindenmayer.generate(axiom, iterations)                 
lindenmayer.turtle_generate(turtle_file, image_file, 
                            start_position, mapping)
