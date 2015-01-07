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
iterations = 6
turtle_file = '19_lindenmayer_tree_turtle.py'
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

count = 1
while count < iterations + 1:
    axiom = lindenmayer.apply_rules(axiom)
    print('Generation %s: Axiom length = %s' % (str(count), str(len(axiom))))
    count = count + 1                   
lindenmayer.turtle_generate(axiom, turtle_file, start_position, mapping)
