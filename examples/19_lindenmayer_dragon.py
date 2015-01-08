'''
Example 19c: Using Lindenmayer system to draw a Dragon Curve
'''
# needed to run this example without prior
# installation of DOSE into Python site-packages
try: 
	import run_examples_without_installation
except ImportError: pass

# Example codes starts from here
import dose, random

axiom = 'FX'
rules = [['X', 'XRYFR'], ['Y', 'LFXLY']]
start_position = (150, 150)
iterations = 12
turtle_file = '19_lindenmayer_dragon_turtle.py'
image_file = '19_lindenmayer_dragon_turtle.svg'
mapping = {'set_angle': 90,
           'random_angle': 0,
           'set_distance': 5,
           'random_distance': 0,
           'background_colour': 'wheat1',
           'F': 'forward',
           'R': 'right',
           'L': 'left'}
           
lindenmayer = dose.lindenmayer(1)
lindenmayer.add_rules(rules)

count = 1
while count < iterations + 1:
    axiom = lindenmayer.apply_rules(axiom)
    print('Generation %s: Axiom length = %s' % (str(count), str(len(axiom))))
    count = count + 1                   
lindenmayer.turtle_generate(axiom, turtle_file, image_file, 
                            start_position, mapping)
