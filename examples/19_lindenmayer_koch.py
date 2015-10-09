'''
Example 19a: Using Lindenmayer system to draw a Koch Curve
'''
# needed to run this example without prior
# installation of DOSE into Python site-packages
try: 
	import run_examples_without_installation
except ImportError: pass

# Example codes starts from here
import dose, random

axiom = 'F'
rules = [['F', 'FRFLFLFRF']]
start_position = (-300, 250)
iterations = 5
turtle_file = '19_lindenmayer_koch_turtle.py'
image_file = '19_lindenmayer_koch_turtle.svg'
mapping = {'set_angle': 90,
           'random_angle': 0,
           'set_distance': 2.5,
           'random_distance': 0,
           'background_colour': 'pale goldenrod',
           'F': 'forward',
           'R': 'right',
           'L': 'left'}
           
lindenmayer = dose.lindenmayer(1)
lindenmayer.add_rules(rules)
lindenmayer.generate(axiom, iterations)                 
lindenmayer.turtle_generate(turtle_file, image_file, 
                            start_position, mapping)
