'''
Example 19b: Using Lindenmayer system to draw a Sierpinski Triangle
'''
# needed to run this example without prior
# installation of DOSE into Python site-packages
try: 
	import run_examples_without_installation
except ImportError: pass

# Example codes starts from here
import dose, random

axiom = 'A'
rules = [['A', 'BLALB'], 
         ['B', 'ARBRA']]
start_position = (-300, 250)
iterations = 8
turtle_file = '19_lindenmayer_sierpinski_turtle.py'
image_file = '19_lindenmayer_sierpinski_turtle.svg'
mapping = {'set_angle': 60,
           'random_angle': 0,
           'set_distance': 2.5,
           'random_distance': 0,
           'background_colour': 'RoyalBlue1',
           'A': 'forward',
           'B': 'forward',
           'R': 'right',
           'L': 'left'}
           
lindenmayer = dose.lindenmayer(1)
lindenmayer.add_rules(rules)
lindenmayer.generate(axiom, iterations)                 
lindenmayer.turtle_generate(turtle_file, image_file, 
                            start_position, mapping)
