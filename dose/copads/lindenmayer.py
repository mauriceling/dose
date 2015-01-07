'''
Framework for Lindenmayer System (L-System)

Copyright (c) Maurice H.T. Ling <mauriceling@acm.org>

Date created: 4th January 2015
'''
import random

import constants

class lindenmayer(object):
    '''
    Lindenmayer system, also commonly known as L-System, is developed 
    by Aristid Lindenmayer in 1968 (reference: Mathematical models for 
    cellular interaction in development. Journal of Theoretical 
    Biology 18:280-315). It is a set of formal grammar of production 
    rules for rewiting an initial axiom or seed text over generations. 
    
    This implementation defines 3 types of rules, also known as production 
    rules or predicates; replacement, probability, and function rules. Each 
    rule can be given a priority.
    
    The simplest form of production rule takes the form of 'A -> BAC', which 
    is read as "whenever 'A' is found, it is replaced/rewritten as 'BAC'". 
    For example, if the starting axiom is "A", then the following will happen
    
        - Generation 0: A
        - Generation 1: BAC
        - Generation 2: BBACC
        - Generation 3: BBBACCC
        - Generation 4: BBBBACCCC
        - and so on.
    
    In this case, the predicate 'A -> BAC' can be written as in 4 different 
    ways - C{['A', 'BAC']}, C{['A', 'BAC', 1]}, C{['A', 'BAC', 1, 
    'replacement']}, or C{['A', 'BAC', 1, 'replacement', 1]}.
    
    When a list of 2-elements is given (e.g., C{['A', 'BAC']}), it is taken 
    to be replacement rule with the highest priority; that is, priority of 1. 
    Hence, C{['A', 'BAC']}, C{['A', 'BAC', 1]}, C{['A', 'BAC', 1, 
    'replacement']}, and C{['A', 'BAC', 1, 'replacement', 1]} are the same. 
    
    This also means that production rules can have different priorities. For 
    example, given C{[['A', 'BAC', 1], ['B', 'BC', 2]]}, rule C{['A', 'BAC', 
    1]} will be executed before C{['B', 'BC', 2]} in the following manner
    
        - Generation 0: A
        - Generation 1: BCAC      # A -> BAC, BAC -> BCAC
        - Generation 2: BCCBCACC
        - Generation 3: BCCCBCCBCACCC
        - and so on as all production rules in ascending order of priorities 
        (with '1' being the highest priority) will be executed in parallel on 
        the resulting axiom at that current point in time.
    
    However, if given C{[['A', 'BAC', 1], ['B', 'BC', 1]]}, then
    
        - Generation 0: A
        - Generation 1: BAC
        - Generation 2: BCBACC
        - Generation 3: BCCBCBACCC
        - Generation 4: BCCCBCCBCBACCCC
        - and so on.
    
    The second form of production rule is probabilistic, also known as 
    stochastic grammars. Probabilistic rule will take the format of 
    C{[<domain>, <range>, <priority>, 'probability', <probability>]}. 
    For example, C{['A', 'BAC', 1, 'probability', 0.5]} means that 'A' 
    will only be rewritten into 'BAC' 50% of the time. 'A' will be left 
    unchanged 50% of the time. The same priority principle applies. 
    Hence, C{['A', 'BAC', 1, 'probability', 1]} is in effect the same as 
    C{['A', 'BAC', 1, 'replacement']}.
    
    The thirs form of production rule is function rule, which takes the 
    form of C{[<domain>, <function>, <priority>, 'function']}. For 
    example, C{['A', axiom_func, 1, 'function']} means that when 'A' is 
    encounted in the axiom, the command string up to that point in time 
    will be used as parameter for axion_func function, such as
    
        - Generation 0: A
        - Generation 1: dependent on the return value of axiom_func('A')
        and so on.
    
    For example, given an axiom of 'ACCCABABDD', and C{['AB', replaceFunction, 
    1, 'function']} as production rule where replaceFunction is defined as 
    
    >>> def replaceFunction(self, dstring, position):
    >>>    if dstring[position+3] == 'O': return 'BAAB'
    >>>    elif dstring[position-1] == 'O': return 'AABB'
    >>>    else: return 'OOAB'
    
        - Generation 0: ACCCABABDD
        - Generation 1: ACCCOOABOOABDD
        - Generation 2: ACCCOOBAABOOAABBDD
        - Generation 3: ACCCOOBABAABOOAABBDD
        - Generation 4: ACCCOOBABABAABOOAABBDD
        - Generation 5: ACCCOOBABABABAABOOAABBDD
    
    In summary, the following rule formats are allowed:
        - C{[<domain>, <range>]}
        - C{[<domain>, <range>, <priority>]}
        - C{[<domain>, <range>, <priority>, 'replacement']}
        - C{[<domain>, <range>, <priority>, 'probability', <probability>]}
        - C{[<domain>, <function>, <priority>, 'function']}
    '''
    def __init__(self, command_length=1, rules=[]):
        '''
        Constructor method.
        
        @param command_length: length of each instruction or command. 
        Default = 1
        @type command_length: integer
        @param rules: a list of list describing the production rules. Please 
        see above for rule syntax. Default is empty list.
        @type rules: list
        '''
        self.command_length = command_length
        self.rules = []
        if len(rules) > 0:
            self.add_rules(rules)
    
    def add_rules(self, rules):
        '''
        Method to add a list of production rules / predicates into the 
        system. 
        
        @param rules: a list of list describing the production rules. Please 
        see above for rule syntax.
        @type rules: list
        '''
        for x in rules:
            if len(x) == 2:
                # [predicate, replacement]
                self.rules.append([x[0], x[1], 1, 'replacement', None])
            elif len(x) == 3:
                # [predicate, replacement, priority]
                self.rules.append([x[0], x[1], int(x[2]), 'replacement', None])
            elif len(x) == 4 and (x[3] not in ['probability', 
                                               'replacement', 
                                               'function']):
                # [predicate, replacement, priority, '<something_else>']
                print('''Warning: Rule type can only be 'probabilistic', \          
                'replacement' or 'function'. Rule, %s, is not added into \ 
                system.''' % str(x))
            elif len(x) == 4 and x[3] == 'replacement':
                # [predicate, replacement, priority, 'replacement']
                self.rules.append([x[0], x[1], int(x[2]), x[3], None])
            elif len(x) == 4 and x[3] == 'probability':
                # [predicate, replacement, priority, 'probability']
                print('''Warning: Function rule will require a \ 
                probability. Rule, %s, is added into system as a \
                replacement rule (100% activation probability).''' % str(x))
                self.rules.append([x[0], x[1], int(x[2]), 'replacement', None])
            elif len(x) == 5 and x[3] == 'probability':
                # [predicate, replacement, priority, 'probability', probability]
                self.rules.append([x[0], x[1], int(x[2]), x[3], float(x[4])])
            elif len(x) == 4 and x[3] == 'function':
                # [predicate, function, priority, 'function']
                self.rules.append([x[0], x[1], int(x[2]), x[3], None])
        self.priority_levels = [x[2] for x in self.rules][-1]
         
    def _apply_priority_rules(self, priority, data_string):
        '''
        Private method - to be used by apply_rules method to apply production 
        rules of a particular priority.
        
        @param priority: order of priority
        @type priority: integer
        @param data_string: data or symbol string to be processed
        @type data_string: string
        @return: rewritten data_string
        '''
        rules = [x for x in self.rules if x[2] == int(priority)]
        ndata = ''
        pointer = 0
        while pointer < len(data_string):
            cmd = data_string[pointer:pointer+self.command_length]
            for rule in rules:
                if cmd == rule[0] and rule[3] == 'replacement':
                    cmd = rule[1]
                    break
                if cmd == rule[0] and rule[3] == 'probability' \
                and random.random() < x[4]:
                    cmd = rule[1]
                    break
                if cmd == rule[0] and rule[3] == 'function':
                    cmd = rule[1](data_string, pointer)
                    break
            if cmd == None: cmd = ''
            ndata = ndata + cmd
            pointer = pointer + self.command_length
        return ndata
            
    def apply_rules(self, data_string):
        '''
        Method to apply all production rules on axiom string (in the first 
        generation) or data/symbol string (in the subsequent generations).
        This method is implemented as a generator.
        
        @param data_string: data or symbol string to be processed
        @type data_string: string
        @return: rewritten data_string
        '''
        for priority in list(range(1, self.priority_levels+1)):
            data_string = self._apply_priority_rules(priority, 
                                                     data_string)
        return data_string

    def turtle_generate(self, data_string, filename=None, 
                        start=(0, 0), mapping={}):
        '''
        Method for naive code generation to visualize the data or symbol 
        string using Turtle graphics. This method generates the Python 
        codes for Turtle graphics using the TK Turtle graphics module, 
        and prints out the resulting Python code as a file.
        
        This method does not use any loops to reduce repetitive Turtle 
        commands; hence, the resulting code file can be huge.
        
        A mapping dictionary is used to convert the symbol string into 
        Turtle commands. The following Turtle commands are defined: 
        forward, backward, right (turn), left (turn), pen up, pen down 
        and home. The default mapping is given as
        
        >>> mapping = {'set_angle': 90,
        >>>            'random_angle': 0,
        >>>            'set_distance': 1,
        >>>            'random_distance': 0,
        >>>            'set_heading': 0,
        >>>            'set_colour': 'black',
        >>>            'background_colour': 'ivory',
        >>>            'F': 'forward',
        >>>            'B': 'backward',
        >>>            'R': 'right',
        >>>            'L': 'left',
        >>>            'H': 'home',
        >>>            'U': 'penup',
        >>>            'D': 'pendown',
        >>>            '[': 'push',
        >>>            ']': 'pop'}
        
        which can be read as 
            - a left or right turn is set at 90 degrees (set_angle). B{This 
            setting is mandatory.}
            - random angles of turn can be set using 'random_angle', where
            the actual angle will be from the set_angle to set_angle + 
            random_angle (by uniform distribution). For example, if 
            random_angle is 10 degrees, it means that the actual angle 
            at each turn will be uniformly distributed from 90 to 100 
            degrees. B{This will be set to 0 if not given.}
            - each forward or backward move is set at 1 (set_distance). 
            B{This setting is mandatory.}
            - random distance of each move can be set using 'random_
            distance', following the same logic as 'random_angle'. B{This 
            will be set to 0 if not given.}
            - turtle is set to head towards 0 degrees (east or to the 
            right of the screen). North (toward top), west (towards left), 
            and south (towards bottom) are 90, 180, 270 degrees 
            respectively. B{This will be set to 0 if not given.}
            - default pen colour can be set using TK colour names as 
            'set_colour'. B{This will be set to black if not given.} Other 
            colours can be set and any un-used symbols (other than 'F', 'B', 
            'R', 'L', 'H', 'U', and 'D') can be used to set pen colours 
            (please see http://wiki.tcl.tk/37701 for available colours).
            - canvas background colour can be set using background_colour. 
            B{This will be set to ivory if not given.}
            - 'F', 'B', 'R', 'L', 'H', 'U', and 'D' represents the Turtle 
            commands of forward, backward, right turn, left turn, home, 
            pen up, and pen down respectively. Home is defined as the start 
            coordinate.
            - '[' pushes the current state (position and heading) of the 
            Turtle into the stack.
            - ']' pops (in a last in first out manner) and sets the Turtle 
            to the last pushed state without drawing the move.
            
        The following colours are defined: snow, ghost white, white smoke, gainsboro, floral white, old lace, linen, antique white, papaya whip, blanched almond, bisque, peach puff, navajo white, moccasin, cornsilk, ivory, lemon chiffon, seashell, honeydew, mint cream, azure, alice blue, lavender, lavender blush, misty rose, white, black, dark slate gray, dim gray, slate gray, light slate gray, gray, light grey, midnight blue, navy, cornflower blue, dark slate blue, slate blue, medium slate blue, light slate blue, medium blue, royal blue, blue, dodger blue, deep sky blue, sky blue, light sky blue, steel blue, light steel blue, light blue, powder blue, pale turquoise, dark turquoise, medium turquoise, turquoise, cyan, light cyan, cadet blue, medium aquamarine, aquamarine, dark green, dark olive green, dark sea green, sea green, medium sea green, light sea green, pale green, spring green, lawn green, green, chartreuse, medium spring green, green yellow, lime green, yellow green, forest green, olive drab, dark khaki, khaki, pale goldenrod, light goldenrod yellow, light yellow, yellow, gold, light goldenrod, goldenrod, dark goldenrod, rosy brown, indian red, saddle brown, sienna, peru, burlywood, beige, wheat, sandy brown, tan, chocolate, firebrick, brown, dark salmon, salmon, light salmon, orange, dark orange, coral, light coral, tomato, orange red, red, hot pink, deep pink, pink, light pink, pale violet red, maroon, medium violet red, violet red, magenta, violet, plum, orchid, medium orchid, dark orchid, dark violet, blue violet, purple, medium purple, thistle, snow2, snow3, snow4, seashell2, seashell3, seashell4, AntiqueWhite1, AntiqueWhite2, AntiqueWhite3, AntiqueWhite4, bisque2, bisque3, bisque4, PeachPuff2, PeachPuff3, PeachPuff4, NavajoWhite2, NavajoWhite3, NavajoWhite4, LemonChiffon2, LemonChiffon3, LemonChiffon4, cornsilk2, cornsilk3, cornsilk4, ivory2, ivory3, ivory4, honeydew2, honeydew3, honeydew4, LavenderBlush2, LavenderBlush3, LavenderBlush4, MistyRose2, MistyRose3, MistyRose4, azure2, azure3, azure4, SlateBlue1, SlateBlue2, SlateBlue3, SlateBlue4, RoyalBlue1, RoyalBlue2, RoyalBlue3, RoyalBlue4, blue2, blue4, DodgerBlue2, DodgerBlue3, DodgerBlue4, SteelBlue1, SteelBlue2, SteelBlue3, SteelBlue4, DeepSkyBlue2, DeepSkyBlue3, DeepSkyBlue4, SkyBlue1, SkyBlue2, SkyBlue3, SkyBlue4, LightSkyBlue1, LightSkyBlue2, LightSkyBlue3, LightSkyBlue4, SlateGray1, SlateGray2, SlateGray3, SlateGray4, LightSteelBlue1, LightSteelBlue2, LightSteelBlue3, LightSteelBlue4, LightBlue1, LightBlue2, LightBlue3, LightBlue4, LightCyan2, LightCyan3, LightCyan4, PaleTurquoise1, PaleTurquoise2, PaleTurquoise3, PaleTurquoise4, CadetBlue1, CadetBlue2, CadetBlue3, CadetBlue4, turquoise1, turquoise2, turquoise3, turquoise4, cyan2, cyan3, cyan4, DarkSlateGray1, DarkSlateGray2, DarkSlateGray3, DarkSlateGray4, aquamarine2, aquamarine4, DarkSeaGreen1, DarkSeaGreen2, DarkSeaGreen3, DarkSeaGreen4, SeaGreen1, SeaGreen2, SeaGreen3, PaleGreen1, PaleGreen2, PaleGreen3, PaleGreen4, SpringGreen2, SpringGreen3, SpringGreen4, green2, green3, green4, chartreuse2, chartreuse3, chartreuse4, OliveDrab1, OliveDrab2, OliveDrab4, DarkOliveGreen1, DarkOliveGreen2, DarkOliveGreen3, DarkOliveGreen4, khaki1, khaki2, khaki3, khaki4, LightGoldenrod1, LightGoldenrod2, LightGoldenrod3, LightGoldenrod4, LightYellow2, LightYellow3, LightYellow4, yellow2, yellow3, yellow4, gold2, gold3, gold4, goldenrod1, goldenrod2, goldenrod3, goldenrod4, DarkGoldenrod1, DarkGoldenrod2, DarkGoldenrod3, DarkGoldenrod4, RosyBrown1, RosyBrown2, RosyBrown3, RosyBrown4, IndianRed1, IndianRed2, IndianRed3, IndianRed4, sienna1, sienna2, sienna3, sienna4, burlywood1, burlywood2, burlywood3, burlywood4, wheat1, wheat2, wheat3, wheat4, tan1, tan2, tan4, chocolate1, chocolate2, chocolate3, firebrick1, firebrick2, firebrick3, firebrick4, brown1, brown2, brown3, brown4, salmon1, salmon2, salmon3, salmon4, LightSalmon2, LightSalmon3, LightSalmon4, orange2, orange3, orange4, DarkOrange1, DarkOrange2, DarkOrange3, DarkOrange4, coral1, coral2, coral3, coral4, tomato2, tomato3, tomato4, OrangeRed2, OrangeRed3, OrangeRed4, red2, red3, red4, DeepPink2, DeepPink3, DeepPink4, HotPink1, HotPink2, HotPink3, HotPink4, pink1, pink2, pink3, pink4, LightPink1, LightPink2, LightPink3, LightPink4, PaleVioletRed1, PaleVioletRed2, PaleVioletRed3, PaleVioletRed4, maroon1, maroon2, maroon3, maroon4, VioletRed1, VioletRed2, VioletRed3, VioletRed4, magenta2, magenta3, magenta4, orchid1, orchid2, orchid3, orchid4, plum1, plum2, plum3, plum4, MediumOrchid1, MediumOrchid2, MediumOrchid3, MediumOrchid4, DarkOrchid1, DarkOrchid2, DarkOrchid3, DarkOrchid4, purple1, purple2, purple3, purple4, MediumPurple1, MediumPurple2, MediumPurple3, MediumPurple4, thistle1, thistle2, thistle3, thistle4, gray1, gray2, gray3, gray4, gray5, gray6, gray7, gray8, gray9, gray10, gray11, gray12, gray13, gray14, gray15, gray16, gray17, gray18, gray19, gray20, gray21, gray22, gray23, gray24, gray25, gray26, gray27, gray28, gray29, gray30, gray31, gray32, gray33, gray34, gray35, gray36, gray37, gray38, gray39, gray40, gray42, gray43, gray44, gray45, gray46, gray47, gray48, gray49, gray50, gray51, gray52, gray53, gray54, gray55, gray56, gray57, gray58, gray59, gray60, gray61, gray62, gray63, gray64, gray65, gray66, gray67, gray68, gray69, gray70, gray71, gray72, gray73, gray74, gray75, gray76, gray77, gray78, gray79, gray80, gray81, gray82, gray83, gray84, gray85, gray86, gray87, gray88, gray89, gray90, gray91, gray92, gray93, gray94, gray95, gray97, gray98, gray99
        
        @param data_string: data or symbol string to be processed
        @type data_string: string
        @param filename: file name to write out the Turtle commands. 
        Default = None, no file will be written
        @type filename: string
        @param start: starting or home coordinate. Default = (0, 0) which 
        is the centre of the TK window
        @type start: tuple
        @param mapping: map to convert the symbol string into Turtle 
        commands. Please see explanation above.
        @type mapping: dictionary
        @return: Python script file of Turtle commands
        '''
        if len(mapping) == 0:
            mapping = {'set_angle': 90,
                       'random_angle': 0,
                       'set_distance': 1,
                       'random_distance': 0,
                       'set_heading': 0,
                       'set_colour': 'black',
                       'background_colour': 'ivory',
                       'F': 'forward',
                       'B': 'backward',
                       'R': 'right',
                       'L': 'left',
                       'H': 'home',
                       '[': 'push',
                       ']': 'pop'}
        stack = []
        if 'random_angle' not in mapping: mapping['random_angle'] = 0
        if 'random_distance' not in mapping: mapping['random_distance'] = 0
        if 'set_heading' not in mapping: mapping['set_heading'] = 0
        if 'set_colour' not in mapping: mapping['set_colour'] = 'black'
        if 'background_colour' not in mapping: mapping['background_colour'] = 'ivory'
        if filename != None:
            f = open(filename, 'w')
            f.write("''' \n")
            f.write('Turtle Graphics Generation from Lindenmayer System \n')
            f.write('in COPADS (http://github.com/copads/copads) \n\n')
            f.write('Code string = %s \n' % (data_string))
            f.write('Code mapping = %s \n' % (mapping))
            f.write("''' \n\n")
            f.write('import turtle \n\n')
            f.write('t = turtle.Turtle() \n')
            f.write('t.setundobuffer(1) \n')
            f.write("turtle.bgcolor('%s') \n" % mapping['background_colour'])
            f.write('t.speed(0) \n\n')
            f.write('t.setheading(%s) \n' % float(mapping['set_heading']))
            f.write('t.penup() \n')
            f.write('t.setposition(%s, %s) \n' % start)
            f.write("t.pencolor('%s') \n" % mapping['set_colour'])
            f.write('t.pendown() \n\n')
        exec('import turtle')
        exec('t = turtle.Turtle()')
        exec('t.setundobuffer(1)')
        exec("turtle.bgcolor('%s')" % mapping['background_colour'])
        exec('t.speed(0)')
        exec('t.setheading(%s)' % float(mapping['set_heading']))
        exec('t.penup()')
        exec('t.setposition(%s, %s)' % start)
        exec("t.pencolor('%s')" % mapping['set_colour'])
        exec('t.pendown()')
        data_string = [cmd for cmd in data_string if cmd in mapping]
        for cmd in data_string:
            if mapping[cmd] == 'push':
                status = [t.position(), t.heading()]
                stack.append(status)
            if mapping[cmd] == 'pop':
                try:
                    status = stack.pop()
                    if filename != None:
                        f.write('t.penup() \n')
                        f.write('t.setposition(%s, %s) \n' % status[0])
                        f.write('t.setheading(%s) \n' % status[1])
                        f.write('t.pendown() \n')
                    exec('t.penup()')
                    exec('t.setposition(%s, %s)' % status[0])
                    exec('t.setheading(%s)' % status[1])
                    exec('t.pendown()')
                except IndexError: pass
            if mapping[cmd] == 'forward': 
                distance = mapping['set_distance'] + \
                           random.random()*mapping['random_distance']
                if filename != None: 
                    f.write('t.forward(%s) \n' % (distance))
                exec('t.forward(%s)' % (distance))
            if mapping[cmd] == 'backward': 
                distance = mapping['set_distance'] + \
                           random.random()*mapping['random_distance']
                if filename != None: 
                    f.write('t.backward(%s) \n' % (distance))
                exec('t.backward(%s)' % (distance))
            if mapping[cmd] == 'home': 
                if filename != None:
                    f.write('t.penup() \n')
                    f.write('t.setposition(%s, %s) \n' % start)
                    f.write('t.pendown()')
                exec('t.penup()')
                exec('t.setposition(%s, %s)' % start)
                exec('t.pendown() \n')
            if mapping[cmd] == 'right':
                angle = mapping['set_angle'] + \
                        random.random()*mapping['random_angle']
                if filename != None:
                    f.write('t.right(%s) \n' % str(angle))
                exec('t.right(%s)' % str(angle))
            if mapping[cmd] == 'left':
                angle = mapping['set_angle'] + \
                        random.random()*mapping['random_angle']
                if filename != None:
                    f.write('t.left(%s) \n' % str(angle))
                exec('t.left(%s)' % str(angle))
            if mapping[cmd] in constants.TKColours:
                f.write("t.pencolor('%s') \n" % mapping[cmd])
                exec("t.pencolor('%s')" % mapping[cmd])
        exec('t.penup()')
        exec('t.setposition(-1000, -1000)')
        exec('turtle.done()')
        if filename != None:
            f.write('\n')
            f.write('t.penup() \n')
            f.write('t.setposition(-1000, -1000) \n')
            f.write('turtle.done() \n')
            f.close()
