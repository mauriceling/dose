'''
Example 19d: Using Lindenmayer system to draw a plant
'''
# needed to run this example without prior
# installation of DOSE into Python site-packages
try: 
	import run_examples_without_installation
except ImportError: pass

# Example codes starts from here
import dose, random

axiom = 'X'
rules = [['X', '0FL[2[X]R3X]R1F[3RFX]LX'],
         ['F', 'FF']]
start_position = (0, -200)
iterations = 6
turtle_file = '19_lindenmayer_plant_turtle.py'
mapping = {'set_angle': 25,
           'random_angle': 0,
           'set_distance': 2.5,
           'random_distance': 0,
           'set_heading': 90,
           'background_colour': 'azure',
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
