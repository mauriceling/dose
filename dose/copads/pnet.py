'''!
Framework for Petri Nets Typed Applications

Date created: 3rd January 2016

License: Python Software Foundation License version 2
'''

class Place(object):
    '''!
    Class to represent a place or container in petri nets. The tokens 
    are represented as a dictionary where each token is represented as 
    a key-value pair. The key represents the type of token and the 
    value represents the number of such tokens. This enables more than 
    one type of tokens to be represented.
    '''
    def __init__(self, name):
        '''!
        Contructor method.
        
        @param name string: name of the place/container
        '''
        self.name = str(name)
        self.attributes = {}
        
class PNet(object):
    '''!
    Class to represent a Petri Net or Petri Net typed object.
    
    The places and transition rules are represented as dictionary 
    objects. Places dictionary will have the name of place as key and 
    the Place (pnet.Place object) as value. Transition rules 
    dictionary will have the name of rule appended with a number (in 
    the format of <rule name>_<number> in order to ensure uniqueness) 
    as key and the value is a dictionary to represent the transition 
    rule (the structure of the transition rule dictionary is dependent 
    on the type of rules).
    
    The following types of transition rules are allowed: 
        - step rule
        - delay rule
        - incubate rule
        - ratio rule
        - function rule
        
    Step rule is to be executed at each time step. For example, if 20g 
    of flour is to be transferred from flour bowl to mixer bowl at 
    each time step, this 'add_flour' rule can be defined as:
    
    >>> net.add_rules('add_flour', 'step', ['flour.flour -> mixer.flour; 20'])
    
    A single step rule can trigger more than one token movement. For 
    example, the following step rule simulates the mixing of 
    ingredients into a flour dough:
    
    >>> net.add_rules('blend', 'step', ['mixer.flour -> mixer.dough; 15', 'mixer.water -> mixer.dough; 10', 'mixer.sugar -> mixer.dough; 0.9', 'mixer.yeast -> mixer.dough; 1'])
                       
    Delay rule acts as a time delay between each token movement. For 
    example, the following rule simulates the transfer of 0.5g of 
    yeast into the mixer bowl:
    
    >>> net.add_rules('add_yeast', 'delay', ['yeast.yeast -> mixer.yeast; 0.5; 10'])
                      
    Incubate rule is a variation of delay rule. While delay rule is 
    not condition dependent, incubate rule starts a time delay when 
    one or more conditions are met. For example,
    
    >>> net.add_rules('rise', 'incubate', ['10; mixer.dough -> pan.dough; mixer.flour == 0; mixer.water == 0; mixer.sugar == 0; mixer.yeast == 0'])
                       
    sets a 10 time step delay when all flour, water, sugar, and yeast 
    in the mixer bowl are used up, which simulates the completemixing 
    into a bread dough. The 10 time step then simulates the time 
    needed for the dough to rise. After 10 time steps, dough in the 
    mixer is transferred into the pan.
    
    Ratio rule is a variant of step rule. Instead of absolute number 
    of tokens to move, the movement is a percentage of the number of 
    tokens. For example, 
    
    >>> net.add_rules('bake', 'ratio', ['pan.dough -> pan.bread; 0.3; pan.dough < 1; 0'])
                      
    will move 30% of the token value from dough in pan to bread in 
    pan. If the token value of dough in pan is less than 1, then the 
    token value of dough in pan will be set to 0.
    
    Function rule is a generic and free-form rule, that takes the form 
    of a Python function. This is usually used when the transition 
    cannot be represented by any other rules. Given a user-defined 
    function, FUNC, 
    
    >>> net.add_rules('cool', 'function', ['table.temperature -> air.temperature', FUNC, 'table.bread > 0; table.temperature > 30'])
                       
    FUNC will be executed when table.bread > 0 and table.temperature > 
    30. The returned result of FUNC will be the token transfer from 
    table.temperature to air.temperature. 
    
    FUNC takes all the places as a single parameter, such as FUNC(
    places), where 'places' is a dictionary with the name of each 
    place as key. Token values in any place can be assessed. For 
    example,
    
    >>> place_names = places.keys()

    >>> a_place = places[places_names[0]]
    
    >>> token_set = a_place.attributes.keys()
    
    >>> a_token_value = a_place.attributes[token_set[0]]
    '''
    def __init__(self, zerolowerbound=True):
        '''!
        Contructor method.
        
        @param zerolowerbound boolean: flag to determine whether 
        number of tokens is bounded at zero. Default = True (the 
        lowest number for tokens is zero)
        '''
        self.places = {}
        self.add_places('ouroboros', {'U': float('inf')})
        self.rules = {}
        self.report = {}
        self.losses = {}
        self.zerolowerbound = zerolowerbound
        self.rulenumber = 1
    
    def add_places(self, place_name, tokens):
        '''!
        Method to add a place/container into the Petri Net.
        
        For example, the following adds a "flour" place containing 
        1000 tokens of flour, which can be seen as a bowl of 1000g of 
        flour:
        
        >>> net.add_places('flour', {'flour': 1000})
        
        @param place_name string: name of the place/container
        @param tokens dictionary: token(s) for the place/container 
        where key is the name/type of token and value is the number of 
        tokens for the specific type
        '''
        self.places[place_name] = Place(place_name)
        self.places[place_name].attributes = tokens
    
    def add_rules(self, rule_name, rule_type, actions):
        '''!
        Method to add a transition rule into the Petri Net.
        
        @param rule_name string: name of the transition rule. This 
        name need not be unique within the model as this method will 
        append a running rule number to the name to ensure internal 
        uniqueness.
        @param rule_type string: type of rule. Allowable types are 
        'step' for step rule, 'delay' for delay rule, and 'incubate' 
        for incubate rule. Please see module documentation for the 
        description of rules.
        @param actions list: describe the action(s) of the transition 
        rule
        '''
        if rule_type not in ['function']:
            for t in actions:
                t = [x.strip() for x in t.split(';')]
                d = {'type': rule_type,
                     'movement': None}
                if rule_type == 'step': 
                    movement = [x.strip() for x in t[0].split('->')]
                    d['movement'] = [(loc.split('.')[0], loc.split('.')[1]) 
                                     for loc in movement]
                    d['value'] = float(t[1])
                if rule_type == 'delay': 
                    movement = [x.strip() for x in t[0].split('->')]
                    d['movement'] = [(loc.split('.')[0], loc.split('.')[1]) 
                                     for loc in movement]
                    d['value'] = float(t[1])
                    d['delay'] = int(t[2])
                if rule_type == 'incubate':
                    d['value'] = float(t[0])
                    movement = [x.strip() for x in t[1].split('->')]
                    d['movement'] = [(loc.split('.')[0], loc.split('.')[1]) 
                                     for loc in movement]
                    d['conditions'] = [cond for cond in t[2:]]
                    d['timer'] = 0
                if rule_type == 'ratio':
                    movement = [x.strip() for x in t[0].split('->')]
                    d['movement'] = [(loc.split('.')[0], loc.split('.')[1]) 
                                     for loc in movement]
                    d['ratio'] = float(t[1])
                    d['limit_check'] = t[2]
                    d['limit_set'] = float(t[3])
                self.rules[rule_name + '_' + str(self.rulenumber)] = d
                self.rulenumber = self.rulenumber + 1
        if rule_type in ['function']:
            d = {'type': rule_type,
                 'movement': None}
            if rule_type == 'function':
                movement = [x.strip() for x in actions[0].split('->')]
                d['movement'] = [(loc.split('.')[0], loc.split('.')[1]) 
                                 for loc in movement]
                d['function'] = actions[1]
                d['conditions'] = [cond.strip() 
                                   for cond in actions[2].split(';')]
            self.rules[rule_name + '_' + str(self.rulenumber)] = d
            self.rulenumber = self.rulenumber + 1
        
    def _step_rule(self, movement, value, interval):
        '''!
        Private method which simulates a step rule action.
        
        @param movement string: defines the movement of a token type. 
        Each movement is defined in the following format: <source 
        place>.<source token> -> <destination place>.<destination 
        token>
        @param value float: the number of tokens to move
        @param interval integer: simulation time interval
        '''
        source_place = self.places[movement[0][0]]
        source_value = movement[0][1]
        destination_place = self.places[movement[1][0]]
        destination_value = movement[1][1]
        if source_place.attributes[source_value] < (value*interval) \
            and self.zerolowerbound == True:
            value = source_place.attributes[source_value]
        source_place.attributes[source_value] = \
            source_place.attributes[source_value] - (value*interval)
        destination_place.attributes[destination_value] = \
            destination_place.attributes[destination_value] + \
            (value*interval)
    
    def _test_condition(self, place, token, operator, value):
        '''!
        Private method used by rule processors for logical check of 
        condition. For example, the condition 'mixer.flour == 0' will 
        be written as 
        
        >>> _test_condition('mixer', 'flour', '==', 0)
        
        @param place string: name of place/container
        @param token string: name of token
        @param operator string: binary operator. Allowable values are 
        '==' (equals to), '>' (more than), '>=' (more than or equals 
        to), '<' (less than), '<=' (less than or equals to), and '!=' (
        not equals to).
        @param value: value to be checked
        @return 'passed' if test result is true, or 0 if test result 
        is false
        '''
        value = float(value)
        if operator == '==' and \
            self.places[place].attributes[token] == value:
            return 'passed'
        elif operator == '>' and \
            self.places[place].attributes[token] > value:
            return 'passed'
        elif operator == '>=' and \
            self.places[place].attributes[token] >= value:
            return 'passed'
        elif operator == '<' and \
            self.places[place].attributes[token] < value:
            return 'passed'
        elif operator == '<=' and \
            self.places[place].attributes[token] <= value:
            return 'passed'
        elif operator == '!=' and \
            self.places[place].attributes[token] != value:
            return 'passed'
        else:
            return 'failed'
    
    def _conditions_processor(self, conditions):
        '''!
        Private method used by rule processors to evaluate logical 
        conditions.
        
        @param conditions list: one or more logical conditions in the 
        format of '<place>.<token> <binary operator> <criterion>', 
        such as 'oven.heat > 300', for evaluation
        '''
        test = [0] * len(conditions)
        for i in range(len(conditions)):
            cond = conditions[i]
            if len(cond.split('==')) == 2:
                operator = '=='
                cond = [c.strip() for c in cond.split('==')]
            elif len(cond.split('>')) == 2:
                operator = '>'
                cond = [c.strip() for c in cond.split('>')]
            elif len(cond.split('>=')) == 2:
                operator = '>='
                cond = [c.strip() for c in cond.split('>=')]
            elif len(cond.split('<')) == 2:
                operator = '<'
                cond = [c.strip() for c in cond.split('<')]
            elif len(cond.split('<=')) == 2:
                operator = '<='
                cond = [c.strip() for c in cond.split('<=')]
            elif len(cond.split('!=')) == 2:
                operator = '!='
                cond = [c.strip() for c in cond.split('!=')]
            source_place = cond[0].split('.')[0]
            source_value = cond[0].split('.')[1]
            criterion = cond[1]
            test[i] = self._test_condition(source_place, source_value, 
                                           operator, criterion)
        return test
        
    def _incubate_rule(self, rule, interval):
        '''!
        Private method which simulates an incubate rule action.
        
        @param rule: a dictionary representing the incubate rule
        @param interval integer: simulation time interval
        @return modified rule dictionary
        '''
        value = rule['value']
        timer = rule['timer']
        conditions = rule['conditions']
        movement = rule['movement']
        test = self._conditions_processor(conditions)
        if len(['failed' for t in test if t == 'failed']) == 0:
            if (timer + interval) < value:
                rule['timer'] = timer + interval
            else:
                source_place = self.places[movement[0][0]]
                source_value = movement[0][1]
                destination_place = self.places[movement[1][0]]
                destination_value = movement[1][1]
                destination_place.attributes[destination_value] = \
                    destination_place.attributes[destination_value] + \
                    source_place.attributes[source_value]
                source_place.attributes[source_value] = 0
                rule['timer'] = 0
        return rule
    
    def _ratio_rule(self, movement, ratio, limit_check, 
                    limit_set, interval):
        '''!
        Private method which simulates a ratio rule action.
        
        @param movement string: defines the movement of a token type. 
        Each movement is defined in the following format: <source 
        place>.<source token> -> <destination place>.<destination 
        token>
        @param ratio float: the ratio of tokens to move
        @param limit_check string: logical check for remainder value
        @param limit_set flaot: value to set token if token in 
        limit_check is true
        @param interval integer: simulation time interval
        '''
        source_place = self.places[movement[0][0]]
        source_value = movement[0][1]
        destination_place = self.places[movement[1][0]]
        destination_value = movement[1][1]
        # Step 1: Perform ratio rule operation
        token_value = source_place.attributes[source_value] * \
                      ratio * interval
        source_place.attributes[source_value] = \
            source_place.attributes[source_value] - token_value
        destination_place.attributes[destination_value] = \
            destination_place.attributes[destination_value] + token_value
        # Step 2: Perform remaining checks and corrections
        if len(limit_check.split('>')) == 2:
            operator = '>'
            limit_check = [c.strip() for c in limit_check.split('>')]
        if len(limit_check.split('<')) == 2:
            operator = '<'
            limit_check = [c.strip() for c in limit_check.split('<')]
        check_place = limit_check[0].split('.')[0]
        check_token = limit_check[0].split('.')[1]
        check_value = float(limit_check[1])
        if self._test_condition(check_place, check_token, 
            operator, check_value) == 'passed':
            if source_value in self.losses:
                self.losses[source_value] = self.losses[source_value] + \
                source_place.attributes[source_value] - limit_set
            else:
                self.losses[source_value] = \
                source_place.attributes[source_value] - limit_set
            source_place.attributes[source_value] = limit_set
    
    def _function_rule(self, movement, function, conditions):
        '''!
        Private method which simulates a function rule action.
        
        @param movement string: defines the movement of a token type. 
        Each movement is defined in the following format: <source 
        place>.<source token> -> <destination place>.<destination 
        token>
        @param function function: a Python function to be executed 
        when conditions are met. This function describes the 
        transition of token.
        @param conditions list: one or more logical conditions in the 
        format of '<place>.<token> <binary operator> <criterion>', 
        such as 'oven.heat > 300', for evaluation
        '''
        source_place = self.places[movement[0][0]]
        source_value = movement[0][1]
        destination_place = self.places[movement[1][0]]
        destination_value = movement[1][1]
        test = self._conditions_processor(conditions)
        if len(['failed' for t in test if t == 'failed']) == 0:
            token_value = function(self.places)
            source_place.attributes[source_value] = \
                source_place.attributes[source_value] - token_value
            destination_place.attributes[destination_value] = \
                destination_place.attributes[destination_value] + token_value
        
    def _execute_rules(self, clock, interval):
        '''!
        Private method used by PNet.simulate() and 
        PNet.simulate_yield() to execute all the rules.
        
        @param clock cloat: wall time of the current simulation
        @param interval integer: simulation time interval
        '''
        affected_places = []
        for rName in self.rules.keys():
            # Step rule
            if self.rules[rName]['type'] == 'step':
                movement = self.rules[rName]['movement']
                value = self.rules[rName]['value']
                self._step_rule(movement, value, interval)
            # Delay rule
            if self.rules[rName]['type'] == 'delay' and \
                (clock % self.rules[rName]['delay']) == 0:
                movement = self.rules[rName]['movement']
                value = self.rules[rName]['value']
                self._step_rule(movement, value, interval)
            # Incubate rule
            if self.rules[rName]['type'] == 'incubate':
                value = self.rules[rName]['value']
                rule = self._incubate_rule(self.rules[rName], interval)
                self.rules[rName] = rule
            # Ratio rule
            if self.rules[rName]['type'] == 'ratio':
                movement = self.rules[rName]['movement']
                ratio = self.rules[rName]['ratio']
                limit_check = self.rules[rName]['limit_check']
                limit_set = self.rules[rName]['limit_set']
                self._ratio_rule(movement, ratio, limit_check, 
                                 limit_set, interval)
            # Function rule
            if self.rules[rName]['type'] == 'function':
                movement = self.rules[rName]['movement']
                conditions = self.rules[rName]['conditions']
                function = self.rules[rName]['function']
                self._function_rule(movement, function, conditions)
       
    def simulate(self, end_time, interval=1.0, report_frequency=1.0):
        '''!
        Method to simulate the Petri Net. This method stores the 
        generated report in memory; hence, not suitable for extended 
        simulations as it can run out of memory. It is possible to 
        conserve memory by reducing the reporting frequency. Use 
        simulate_yield method for extended simulations.
        
        @param end_time integer: number of time steps to simulate. If 
        end_time = 1000, it can be 1000 seconds or 1000 days, 
        depending on the significance of each step
        @param interval float: number of intervals between each time 
        step. Default = 1.0, simulate by time step interval
        @param report_frequency float: number of time steps between 
        each reporting. Default = 1.0, each time step is reported
        '''
        clock = 1
        end_time = int(end_time)
        while clock < (end_time + 1):
            self._execute_rules(clock, interval)
            if (clock % report_frequency) == 0: 
                self._generate_report(clock)
            clock = clock + interval

    def simulate_yield(self, end_time, interval=1.0):
        '''!
        Method to simulate the Petri Net. This method runs as a 
        generator, making it suitable for extended simulation.
        
        @param end_time integer: number of time steps to simulate. If 
        end_time = 1000, it can be 1000 seconds or 1000 days, 
        depending on the significance of each step
        @param interval float: number of intervals between each time 
        step. Default = 1.0, simulate by time step interval
        '''
        clock = 1
        end_time = int(end_time)
        while clock < end_time:
            self._execute_rules(clock, interval)
            self._generate_report(clock)
            rept = {}
            for k in self.report[str(clock)].keys():
                rept[k] = self.report[str(clock)][k]
            del self.report[str(clock)][k]
            yield (clock, rept)
            clock = clock + interval
                
    def _generate_report(self, clock):
        '''!
        Private method to generate and store report in memory of each 
        token status (the value of each token) in every place/
        container.
        
        @param clock float: step count of the current simulation
        '''
        rept = {}
        for pName in self.places.keys():
            for aName in self.places[pName].attributes.keys():
                value = self.places[pName].attributes[aName]
                name = '.'.join([pName, aName])
                rept[name] = value
        self.report[str(clock)] = rept
        
    def report_tokens(self, reportdict=None):
        '''!
        Method to report the status of each token(s) from each place 
        as a list. This can be used in 2 different ways: to generate a 
        list representation of a status from one time step (such as 
        from simulate_yield method), or to generate a list 
        representation of a status from entire simulation (such as 
        from simulate method). 
        
        from simulate method
        >>> net.simulate(65, 1, 1)
        
        >>> status = net.report_tokens()
        
        from simulate_yield method
        >>> status = [d for d in net.simulate_yield(65, 1)]
        
        >>> status = [(d[0], net.report_tokens(d[1])) for d in status]
        
        @param reportdict dictionary: status from one time step. 
        Default = None. If None, it will assume that simulate method 
        had been executed and all status are stored in memory, and 
        this method will generate a report from status stored in memory
        @return tuple of ([<place.token name>], [([<place.token 
        value>]]) if reportdict is given, or tuple of (time step, [<
        place.token name>], [([<place.token value>]]) if reportdict is 
        None.
        '''
        if reportdict:
            placetokens = reportdict.keys()
            tokenvalues = [reportdict[k] for k in placetokens]
            return (placetokens, tokenvalues)
        else:
            timelist = list(self.report.keys())
            datalist = [0] * len(timelist)
            for i in range(len(timelist)):
                placetokens = list(self.report[timelist[i]].keys())
                tokenvalues = [self.report[timelist[i]][k] 
                               for k in placetokens]
                datalist[i] = (timelist[i], placetokens, tokenvalues)
            return datalist
        