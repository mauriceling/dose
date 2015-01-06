'''
Framework for Lindenmayer System (L-System)

Copyright (c) Maurice H.T. Ling <mauriceling@acm.org>

Date created: 4th January 2015
'''
import random

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

    def turtle_generate(self, data_string, filename, 
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
        forward, backward, right (turn), left (turn), and home. The 
        default mapping is given as
        
        >>> mapping = {'set_angle': 90,
        >>>            'random_angle': 0,
        >>>            'set_distance': 1,
        >>>            'random_distance': 0,
        >>>            'F': 'forward',
        >>>            'B': 'backward',
        >>>            'R': 'right',
        >>>            'L': 'left',
        >>>            'H': 'home'}
        
        which can be read as 
            - a left or right turn is set at 90 degrees (set_angle).
            - random angles of turn can be set using 'random_angle', where
            the actual angle will be from the set_angle to set_angle + 
            random_angle (by uniform distribution). For example, if 
            random_angle is 10 degrees, it means that the actual angle 
            at each turn will be uniformly distributed from 90 to 100 
            degrees.
            - each forward or backward move is set at 1 (set_distance).
            - random distance of each move can be set using 'random_
            distance', following the same logic as 'random_angle'.
            - 'F', 'B', 'R', 'L', and 'H' represents the Turtle commands 
            of forward, backward, right turn, left turn, and home 
            respectively. Home is defined as the start coordinate.
            
        @param data_string: data or symbol string to be processed
        @type data_string: string
        @param filename: file name to write out the Turtle commands
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
                       'F': 'forward',
                       'B': 'backward',
                       'R': 'right',
                       'L': 'left',
                       'H': 'home'}
        if 'random_angle' not in mapping: mapping['random_rangle'] = 0
        f = open(filename, 'w')
        f.write("''' \n")
        f.write('Turtle Graphics Generation from Lindenmayer System \n')
        f.write('in COPADS (http://github.com/copads/copads) \n\n')
        f.write('Code string = %s \n' % (data_string))
        f.write('Code mapping = %s \n' % (mapping))
        f.write("''' \n\n")
        f.write('import turtle \n\n')
        f.write('t = turtle.Turtle() \n')
        f.write('t.speed(0) \n\n')
        f.write('t.penup() \n')
        f.write('t.setposition(%s, %s) \n' % start)
        f.write('t.pendown() \n\n')
        data_string = [cmd for cmd in data_string if cmd in mapping]
        for cmd in data_string:
            if mapping[cmd] == 'forward': 
                distance = mapping['set_distance'] + \
                           random.random()*mapping['random_distance']
                f.write('t.forward(%s) \n' % (distance))
            if mapping[cmd] == 'backward': 
                distance = mapping['set_distance'] + \
                           random.random()*mapping['random_distance']
                f.write('t.backward(%s) \n' % (distance))
            if mapping[cmd] == 'home': 
                f.write('t.penup() \n')
                f.write('t.setposition(%s, %s) \n' % start)
                f.write('t.pendown() \n')
            if mapping[cmd] == 'right':
                angle = mapping['set_angle'] + \
                        random.random()*mapping['random_angle']
                f.write('t.right(%s) \n' % str(angle))
            if mapping[cmd] == 'left':
                angle = mapping['set_angle'] + \
                        random.random()*mapping['random_angle']
                f.write('t.left(%s) \n' % str(angle))
        f.write('\n')
        f.write('turtle.done() \n')
        f.close()
