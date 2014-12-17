'''
Standalone command line system for DOSE.

Date created: 22nd October 2013
'''
import os, sys, copy, random, traceback
from datetime import datetime

# attempt to import readline or pyreadline
try:
    import readline
    readline_import = True
    pyreadline_import = False
except ImportError:
    readline_import = False
    try:
        import pyreadline as readline
        pyreadline_import = True
    except ImportError:
        readline_import = False
        pyreadline_import = False
    
import dose

def quotation():
    quotations = [
'''An expert is a person who has made all the mistakes that can be made in 
a very narrow field.
  -- Niels Bohr''',
'''Touch a scientist and you touch a child.
  -- Ray Bradbury''',
'''There are no shortcuts in evolution.
  -- Louis D. Brandeis''',
'''If you imagine the 4,500-billion-odd years of Earth's history compressed 
into a normal earthly day, then life begins very early, about 4 A.M., with 
the rise of the first simple, single-celled organisms, but then advances no 
further for the next sixteen hours. Not until almost 8:30 in the evening, 
with the day five-sixths over, has Earth anything to show the universe but 
a restless skin of microbes. Then, finally, the first sea plants appear, 
followed twenty minutes later by the first jellyfish and the enigmatic 
Ediacaran fauna first seen by Reginald Sprigg in Australia. At 9:04 P.M. 
trilobites swim onto the scene, followed more or less immediately by the 
shapely creatures of the Burgess Shale. Just before 10 P.M. plants begin to 
pop up on the land. Soon after, with less than two hours left in the day, 
the first land creatures follow.

Thanks to ten minutes or so of balmy weather, by 10:24 the Earth is covered 
in the great carboniferous forests whose residues give us all our coal, and 
the first winged insects are evident. Dinosaurs plod onto the scene just 
before 11 P.M. and hold sway for about three-quarters of an hour. At 
twenty-one minutes to midnight they vanish and the age of mammals begins. 
Humans emerge one minute and seventeen seconds before midnight. The whole 
of our recorded history, on this scale, would be no more than a few seconds, 
a single human lifetime barely an instant. Throughout this greatly speeded-up 
day continents slide about and bang together at a clip that seems positively 
reckless. Mountains rise and melt away, ocean basins come and go, ice sheets 
advance and withdraw. And throughout the whole, about three times every 
minute, somewhere on the planet there is a flash-bulb pop of light marking 
the impact of a Manson-sized meteor or one even larger. It's a wonder that 
anything at all can survive in such a pummeled and unsettled environment. 
In fact, not 
many things do for long.
  -- Bill Bryson''',
'''A true scientist is working at the very limit of his own knowledge, 
and therefore half of the time he is feeling incompetent. Our job is to feel 
incompetent 50% of the time, by pushing the boundary. When we are feeling 
completely comfortable and competent, we are not doing our job.
  -- Carlos Bustamante''',
'''Science is wonderfully equipped to answer the question 'How?' 
but it gets terribly confused when you ask the question 'Why?'
  -- Erwin Chargaff''',
'''When you're thirsty and it seems that you could drink the entire ocean that's faith; 
when you start to drink and finish only a glass or two that's science.
  -- Anton Chekhov''',
'''If an elderly but distinguished scientist says that something is possible, 
he is almost certainly right; 
but if he says that it is impossible, 
he is very probably wrong.
  -- Arthur C. Clarke''',
'''What is a scientist after all? 
It is a curious man looking through a keyhole, the keyhole of nature, 
trying to know what's going on.
  -- Jacques Yves Cousteau''',
'''It is not the strongest of the species that survives, 
nor the most intelligent that survives. 
It is the one that is the most adaptable to change.
  -- Charles Darwin''',
'''I have called this principle, by which each slight variation, 
if useful, is preserved, by the term of Natural Selection.
  -- Charles Darwin''',
'''False facts are highly injurious to the progress of science, 
for they often endure long; 
but false views, if supported by some evidence, do little harm, 
for every one takes a salutary pleasure in proving their falseness.
  -- Charles Darwin ''',
'''Multiply, vary, let the strongest live and the weakest die.
  -- Charles Darwin''',
'''By all means let's be open-minded, 
but not so open-minded that our brains drop out.
  -- Richard Dawkins''',
'''Personally, I rather look forward to a computer program winning the 
world chess championship. Humanity needs a lesson in humility.
  -- Richard Dawkins''',
'''Natural selection is anything but random.
  -- Richard Dawkins''',
'''The theory of evolution by cumulative natural selection is the only 
theory we know of that is in principle capable of explaining the existence 
of organized complexity.
  -- Richard Dawkins''',
'''Gravity is not a version of the truth. It is the truth. 
Anyone who doubts it is invited to jump out a tenth-storey window.
  -- Richard Dawkins''',
'''The chicken is only an egg's way for making another egg.
  -- Richard Dawkins''',
'''Evolution could so easily be disproved if just a single fossil turned up 
in the wrong date order. Evolution has passed this test with flying colours.
  -- Richard Dawkins''',
'''Evolution is not a genetically controlled distortion of one adult form 
into another; it is a genetically controlled alteration in a developmental 
program.
  -- Richard Dawkins''',
'''Computer science is no more about computers than astronomy is about telescopes.
  -- Edsger Dijkstra''',
'''To invent, you need a good imagination and a pile of junk.
  -- Thomas Edison''',
'''Only two things are infinite, the universe and human stupidity, 
and I'm not sure about the former.
  -- Albert Einstein''',
'''No amount of experimentation can ever prove me right; 
a single experiment can prove me wrong.
  -- Albert Einstein''',
'''Never memorize something that you can look up.
  -- Albert Einstein''',
'''If we knew what it was we were doing, it would not be called research, 
would it?
  -- Albert Einstein''',
'''Men love to wonder, and that is the seed of science.
  -- Ralph Waldo Emerson''',
'''There are two possible outcomes: 
if the result confirms the hypothesis, then you've made a measurement.
If the result is contrary to the hypothesis, then you've made a discovery.
  -- Enrico Fermi''',
'''Physics is like sex. Sure, it may give some practical results, 
but that's not why we do it.
  -- Richard Feynman''',
'''The Bible shows the way to go to heaven, not the way the heavens go.
  -- Galileo Galilei''',
'''Chimps are very quick to have a sudden fight or aggressive episode, 
but they're equally as good at reconciliation.
 -- Jane Goodall''',
'''The improver of natural knowledge absolutely refuses to acknowledge 
authority, as such. For him, skepticism is the highest of duties; 
blind faith the one unpardonable sin.
  -- Thomas Huxley''',
'''The ultimate court of appeal is observation and experiment... 
not authority.
  -- Thomas Huxley''',
'''The medieval university looked backwards; it professed to be a storehouse 
of old knowledge. The modern university looks forward, and is a factory of 
new knowledge.
  -- Thomas Huxley''',
'''A straight line is not the shortest distance between two points.
  - Madeleine L'Engle''',
'''It is not always the magnitude of the differences observed between species 
that must determine specific distinctions, but the constant preservation of 
those differences in reproduction.
  -- Jean-Baptiste Lamarck''',
'''Science has proof without any certainty. 
Creationists have certainty without any proof.
  -- Ashley Montague''',
'''Anyone who attempts to generate random numbers by deterministic means is, 
of course, living in a state of sin.
  -- John von Neumann''',
'''To me there has never been a higher source of earthly honor or distinction 
than that connected with advances in science.
  -- Isaac Newton''',
'''If I have seen further than others, 
it is by standing upon the shoulders of giants.
  -- Isaac Newton''',
'''Science is built up of facts, as a house is built of stones; 
but an accumulation of facts is no more a science than a heap of stones is a house.
  -- Henri Poincare''',
'''Science is not only compatible with spirituality; it is a profound source 
of spirituality.
  -- Carl Sagan''',
'''We are all star stuff.
  -- Carl Sagan''',
'''If you cannot - in the long run - tell everyone what you have been doing, 
your doing has been worthless.
  -- Erwin Schrodinger''']
    return random.choice(quotations)

class DOSECommandShell(object):
    
    commands = ('connectdb',
                'copyright', 
                'credits',
                'flush',
                'help', 
                'license',
                'list',
                'quit',
                'py',
                'pyshell',
                'save',
                'show',)
    
    def __init__(self):
        self.history = {}
        self.results = {}
        self.userdata = {}
        self.environment = {'command_count': 0,
                            'cwd': os.getcwd(),
                            'database_connector': None,
                            'database_cursor': None,
                            'database_file': None,
                            'last_command_time': None,
                            'readline_module': None,
                            'starting_time': str(datetime.utcnow()),
                           }
    
    def do_connectdb(self, option, param, count):
        '''
Command: connectdb <options> <file name>
    <options> = {absolute | cwd}
    <file name> = File name for simulation logging database. If the database 
                  file is not found, it will be created.
Description: Establish connection to a simulation logging database.
Pre-requisite(s): None

<options> = absolute
    Defines absolute file path for <file name> to simulation logging database.
<options> = cwd
    Defines relative file path for <file name> to simulation logging database.
    <file name> will be prefixed with current working directory in the format
    of <current working directory>/<file name>'''
        if param == '':
            error_message = 'Error: 2 options needed; %s provided' % len(arg)
            self.history[str(count)] = self.history[str(count)] + \
                                       ' | ' + error_message
            print(error_message)
            print(self.do_connectdb.__doc__)
            return
        elif option == 'absolute':
            self.environment['database_file'] = param
            (con, cur) = dose.connect_database(param, None)
            self.environment['database_connector'] = con
            self.environment['database_cursor'] = cur
        elif option == 'cwd':
            path = os.sep.join([self.environment['cwd'], param])
            self.environment['database_file'] = path
            (con, cur) = dose.connect_database(path, None)
            self.environment['database_connector'] = con
            self.environment['database_cursor'] = cur
        else:
            txt = option + ' is not a valid option. Type help connectdb for more information'
            self.results[count] = txt
            print(txt)

    def do_copyright(self, option, param, count):
        print()
        print('Copyright 2010-2013, Maurice HT Ling (on behalf of all authors)')
        print()
    
    def do_credits(self, option, param, count):
        print()
        print('''DOSE Project Team
Project architect: Maurice HT Ling (mauriceling@acm.org)
Lead developer: Clarence Castillo''')
        print()
    
    def do_flush(self, option, param, count):
        '''
Command: flush <options>
<options> = {data | data <item> | userdata | userdata <key>}
Description: Deletes / clears internal variables
Pre-requisite(s): None

<options> = data
    Delete all results/data (self.results) in the current session
<options> = data <item>
    Delete only specific result/data (self.results), where <item> is the 
    command number
<options> = userdata
    Delete all user-defined data (self.userdata) in the current session
<options> = userdata <key>
    Delete only specific user-defined data (self.userdata), where <key> 
    is the dictionary key
        '''
        if option == '': 
            self.no_options_error_message(self.do_flush, count)
        elif option == 'data' and param == '':
            self.results = {}
            print('All data cleared (from self.results)')
        elif option == 'data' and param != '':
            if self.results.pop(str(param), None) != None:
                print('Data (self.results) cleared from Key = ', str(param))
            else:
                print('Item = ', str(param), ' does not exist in self.results')
        elif option == 'userdata' and param == '':
            self.userdata = {}
            print('All user-defined data cleared (from self.userdata)')
        elif option == 'userdata' and param != '':
            if self.userdata.pop(str(param), None) != None:
                print('User-defined data (self.userdata) cleared from Key = ', str(param))
            else:
                print('Key = ', str(param), ' does not exist in \
user-defined data (self.userdata)')
        
    def do_help(self, option, param, count):
        '''
List of available commands:
connectdb           copyright           credits          flush
help                license             list             py  
pyshell             quit                save             show

Type help <command> for more help (if any)'''
        if option == '' or option == 'help': print(self.do_help.__doc__)
        elif option == 'connectdb': print(self.do_connectdb.__doc__)
        elif option == 'copyright': self.do_copyright(option, param, count)
        elif option == 'credits': self.do_credits(option, param, count)
        elif option == 'flush': self.do_flush.__doc__
        elif option == 'license': self.do_license(option, param, count)
        elif option == 'list': print(self.do_list.__doc__)
        elif option == 'quit': print(self.do_quit.__doc__)
        elif option == 'py': print(self.do_py.__doc__)
        elif option == 'pyshell': print(self.do_pyshell.__doc__)
        elif option == 'save': print(self.do_save.__doc__)
        elif option == 'show': print(self.do_show.__doc__)
        else:
            txt = option + ' is not a valid command; hence, no help is available.'
            self.results[count] = txt
            print(txt)
    
    def do_license(self, option, param, count):
        print()
        print('''
DOSE License: Unless otherwise specified, all files in dose/copads folder 
will be licensed under Python Software Foundation License version 2.
All other files, including DOSE, will be GNU General Public License version 3.''')
        print()
        
    def do_list(self, option, param, count):
        '''
Command: list <options>
    <options> = {generations | popname | simulations}
Description: Display information about simulations logged in the simulation 
    logging database.
Pre-requisite(s): Requires connection to a simulation logging database 
(using connectdb command)

<options> = datafields <start_time> <table>
    List all logged datafields of a simulation (identified by start_time) 
    from one of the 4 tables (parameters, organisms, world, and miscellaneous) 
    in the simulation logging database. If <table> is not given, generations 
    will be listed from organisms table.
<options> = generations <start_time> <table>
    List all logged generations of a simulation (identified by start_time) 
    from one of the 3 tables (organisms, world, and miscellaneous) in the 
    simulation logging database. If <table> is not given, generations will 
    be listed from organisms table.
<options> = simulations
    List all simulations in the simulation logging database, in the format 
    of [<starting time of simulation>, <simulation name>]
<options> = popname
    List all logged population names of a simulation (identified by 
    start_time) in the simulation logging database.
        '''
        cur = self.environment['database_cursor']
        param = [x.strip() for x in param.split(' ')]
        if len(param) == 1: table = 'organisms'
        else: table = param[1]
        if cur == None:
            error_message = 'Error: no database had been connected'
        if option == '':
            self.no_options_error_message(self.do_list, count)
        elif option == 'datafields':
            print('''Searching for data fields logged in simulation
    start time = %s of 
    simulation logging database file = %s
    table = %s''' % (param[0], self.environment['database_file'], table))
            results = dose.db_list_datafields(cur, param[0], table)
            self.results[count] = results
            for r in results: print(r)
        elif option == 'generations':
            print('''Searching for generations logged in simulation
    start time = %s of 
    simulation logging database file = %s
    table = %s''' % (param[0], self.environment['database_file'], table))
            results = dose.db_list_generations(cur, param[0], table)
            self.results[count] = results
            for r in results: print(r)
        elif option == 'popname': 
            print('''Searching for population names logged in simulation
    start time = %s of 
    simulation logging database file = %s''' % (param[0], self.environment['database_file']))
            results = dose.db_list_population_name(cur, param[0])
            self.results[count] = results
            for r in results: print(r)
        elif option == 'simulations': 
            print('''Searching for simulations logged in simulation logging 
database file = %s''' % (self.environment['database_file']))
            results = dose.db_list_simulations(cur)
            self.results[count] = results
            for r in results: print(r)
        else:
            txt = option + ' is not a valid option. Type help list for more information'
            self.results[count] = txt
            print(txt)
            
    def do_py(self, option, param, count):
        '''
Command: py <python statement>
    <python statement> = any fully formed and complete Python statement in 
                         a single line (not for multi-line statement, such 
                         as loop)
Description: Execute an arbitrary single-lined Python statement
Pre-requisite(s): None
        '''
        exec(arg)
        
    def do_pyshell(self, option, param, count):
        '''
Command: pyshell
Description: Launch a full Python interactive interpreter and exposes 
    current DOSE command shell as 'self' object. The 3 main dictionaries in 
    current DOSE command shell are exposed at top level - 
    (1) environment (from self.environment - a dictionary that holds all 
    environmental variables), 
    (2) results (from self.results - a dictionary that results from each 
    command in the current session if any), and 
    (3) userdata (from self.userdata - a dictionary that holds any user 
    defined data). 
    This command provides full functionality to the user, which is similar 
    to using DOSE as a library. Hence, please read DOSE command shell 
    documentation and use with care.
    To exit from the interactive interpreter, use Crtl-D.
Pre-requisite(s): None
        '''
        exec('''import code; \
                import dose; \
                environment = self.environment; \
                userdata = self.userdata;\
                results = self.results;\
                code.interact(local=vars())''')
        
    def do_quit(self, option, param, count):
        '''
Command: quit
Description: Terminate this application
Pre-requisite(s): None'''
        print()
        print('''Are you going off?? -:(
Please contact Maurice Ling (mauriceling@acm.org) if you need any help.
Goodbye! Have a nice day and hope to see you again soon!

%s

Current time is %s''' % (quotation(), str(datetime.utcnow())))
        print()
        
    def do_save(self, option, param, count):
        '''
Command: save <options> <file name>
    <options> = {history | workspace}
    <file name> = File name for output. The file will be in current working
                  directory
Description: To save history or data into a text file
Pre-requisite(s): None

<options> = history
    Writes out history of the current session into <file name>
<options> = workspace
    Writes out the entire workspace (history, data, environment) of the 
    current session into <file name>'''
        if option == '':
            self.no_options_error_message(self.do_save, count)
        if param == '': 
            param = 'saved.' + str(self.environment['starting_time']) + '.txt'
        outfile = open(os.sep.join([str(self.environment['cwd']), param]), 'a')
        if option == 'history':
            outfile.write('Date time stamp of current session: ' + \
                         str(self.environment['starting_time']) + os.linesep)
            keys = [int(x) for x in list(self.history.keys())]
            keys.sort()
            for k in [str(x) for x in keys]:
                txt = ' | '.join(['Command', k, str(self.history[k])])
                outfile.write(txt + os.linesep)
            outfile.write('===================================' + os.linesep)
            outfile.close()
        elif option == 'workspace':
            outfile.write('Date time stamp of current session: ' + \
                         str(self.environment['starting_time']) + os.linesep)
            # writing out environment
            for k in list(self.environment.keys()):
                txt = ['Environment', str(k), str(self.environment[k])]
                txt = ' | '.join(txt)
                outfile.write(txt + os.linesep)
            # prepare to write out commands and data
            historykeys = list(self.history.keys())
            keys = [x for x in list(self.results.keys()) 
                    if x not in historykeys]
            keys = keys + historykeys
            keys = [int(x) for x in keys]
            keys.sort()
            for k in [str(x) for x in keys]:
                # writing out commands
                txt = ' | '.join(['Command', k, str(self.history[k])])
                outfile.write(txt + os.linesep)
                # writing out data (self.results) if any
                try:
                    txt = ' | '.join(['Data', str(k), str(self.results[k])])
                    outfile.write(txt + os.linesep)
                except: pass
            outfile.write('===================================' + os.linesep)
            outfile.close()
        else:
            txt = option + ' is not a valid option. Type help save for more information'
            self.results[count] = txt
            print(txt)
            
    def do_show(self, option, param, count):
        '''
Command: show <options>
    <options> = {data | data <item> | environment | history | history <item> |
                 memory data | memory userdata | userdata | userdata <key>}
Description: Display internal variables
Pre-requisite(s): None

<options> = data
    Display all results/data (self.results) in the current session, in the 
    format of Count = <command number> | Data = <data/results in text format>
<options> = data <item>
    Display only specific result/data (self.results), where <item> is the 
    command number
<options> = environment
    Display all environmental variables in DOSE command shell as one line 
    per environmental variable.
<options> = history
    Display all history in the current session, in the format of 
    Count = <command number> | Command = <command string>
<options> = history <item>
    Display only specific historical command, where <item> is the command 
    number
<options> = memory data
    Display memory size of each data element of result/data (self.results).
<options> = memory userdata
    Display memory size of each data element of user-specific data 
    (self.userdata).
<options> = userdata
    Display all user-defined data (self.userdata) in the current session, 
    in the format of Key = <dictionary key> | Data = <data/results in text 
    format>
<options> = userdata <key>
    Display only specific user-defined data (self.userdata), where <key> 
    is the dictionary key'''
        if option == '':
            self.no_options_error_message(self.do_show, count)
        elif option == 'environment':
            self.results[count] = copy.deepcopy(self.environment)
            print('Environment variables:')
            for key in list(self.environment.keys()):
                print(key, '=', self.environment[key])
        elif option == 'history' and param == '':
            self.results[count] = copy.deepcopy(self.history)
            keys = [int(x) for x in list(self.history.keys())]
            keys.sort()
            for k in [str(x) for x in keys]:
                print('Count =', k, '| Command =', self.history[k])
        elif option == 'history' and param != '':
            self.results[count] = self.history[str(param)]
            print('Count =', param, '| Command =', self.history[str(param)])
        elif option == 'data' and param == '':
            keys = [int(x) for x in list(self.results.keys())]
            keys.sort()
            for k in [str(x) for x in keys]:
                print('Count =', k, '| Data =', self.results[k])
        elif option == 'data' and param != '':
            self.results[count] = self.results[str(param)]
            print('Count =', param, '| Data =', self.results[str(param)])
        elif option == 'userdata' and param == '':
            keys = [int(x) for x in list(self.userdata.keys())]
            keys.sort()
            for k in [str(x) for x in keys]:
                print('Key =', k, '| Data =', self.userdata[k])
        elif option == 'userdata' and param != '':
            self.results[count] = self.userdata[str(param)]
            print('Key =', param, '| Data =', self.userdata[str(param)])
        elif option == 'memory' and param == 'data':
            keys = [int(x) for x in list(self.results.keys())]
            keys.sort()
            for k in [str(x) for x in keys]:
                print('Data (self.results) memory usage (Count = %s): %s bytes' % (k, 
                                                      sys.getsizeof(self.results[k])))
        elif option == 'memory' and param == 'userdata':
            keys = [int(x) for x in list(self.userdata.keys())]
            keys.sort()
            for k in [str(x) for x in keys]:
                print('''User-defined data (self.userdata) memory usage \
(Count = %s): %s bytes''' % (k, sys.getsizeof(self.userdata[k])))
        else:
            txt = option + ' is not a valid option. Type help show for more information'
            self.results[count] = txt
            print(txt)
    
    def no_options_error_message(self, function, count):
        error_message = 'Error: No options provided'
        self.history[str(count)] = self.history[str(count)] + \
                                   ' | ' + error_message
        print(error_message)
        print(function.__doc__)
                
    def command_handler(self, cmd, option, param, count):
        count = str(count)
        if cmd == 'connectdb': self.do_connectdb(option, param, count)
        elif cmd == 'copyright': self.do_copyright(option, param, count)
        elif cmd == 'credits': self.do_credits(option, param, count)
        elif cmd == 'help': self.do_help(option, param, count)
        elif cmd == 'flush': self.do_flush(option, param, count)
        elif cmd == 'license': self.do_license(option, param, count)
        elif cmd == 'list': self.do_list(option, param, count)
        elif cmd == 'py': self.do_py(option, param, count)
        elif cmd == 'pyshell': self.do_pyshell(option, param, count)
        elif cmd == 'quit': self.do_quit(option, param, count)
        elif cmd == 'save': self.do_save(option, param, count)
        elif cmd == 'show': self.do_show(option, param, count)
    
    def cmdloop(self):
        statement = ''
        count = 1
        while True:
            try:
                statement = raw_input("DOSE:%s > " % str(count))
                statement = str(statement.strip())
                statement = statement.lower()
                self.history[str(count)] = statement
                statement = [x.strip() for x in statement.split(' ')]
                cmd = statement[0]
                if len(statement) == 1: 
                    option = ''
                    param = ''
                elif len(statement) == 2:
                    option = statement[1]
                    param = ''
                elif len(statement) == 3:
                    option = statement[1]
                    param = statement[2]
                else:
                    option = statement[1]
                    param = ' '.join(statement[2:])
                if cmd in self.commands:
                    self.environment['last_command_time'] = str(datetime.utcnow())
                    self.environment['command_count'] = count
                    self.command_handler(cmd, option, param, count)
                else:
                    error_message = cmd + ' is not a valid command.'
                    self.history[str(count)] = self.history[str(count)] + \
                        ' | Error message: ' + error_message
                    print(error_message)
                if cmd == 'quit':
                    break
                count = count + 1
            except:
                error_message = list(self.formatExceptionInfo())
                self.results[str(count)] = error_message
                for line in error_message:
                    if (type(line) == list):
                        for l in line: print(l)
                    print(line)
                
    def completer(self, text, state):
        options = [x for x in self.commands 
                   if x.startswith(text)]
        try: return options[state]
        except IndexError: return None
    
    def header(self):
        print('''
Digital Organisms Simulation Environment (DOSE), version 0.1
Current time is %s

%s

Type "help", "copyright", "credits" or "license" for more information.
To exit this application, type "quit".
''' % (self.environment['starting_time'], quotation()))
    
    def formatExceptionInfo(self, maxTBlevel=10):
        """
        Method to gather information about an exception raised. It is used
        to readout the exception messages and type of exception. This method
        takes a parameter, maxTBlevel, which is set to 10, which defines the
        maximum level of tracebacks to recall.
        
        This method is obtained from http://www.linuxjournal.com/
        article.php?sid=5821"""
        cla, exc, trbk = sys.exc_info()
        excName = cla.__name__
        try: excArgs = exc.__dict__["args"]
        except KeyError: excArgs = "<no args>"
        excTb = traceback.format_tb(trbk, maxTBlevel)
        return (excName, excArgs, excTb)

            
if __name__ == '__main__':
    shell = DOSECommandShell()
    shell.header()
    if readline_import:
        shell.environment['readline_module'] = 'readline'
    elif pyreadline_import:
        shell.environment['readline_module'] = 'pyreadline'
    else:
        shell.environment['readline_module'] = None
    if readline_import or pyreadline_import:
        readline.set_completer(shell.completer)   # enables autocompletion
        readline.parse_and_bind("tab: complete")
    shell.cmdloop()
    sys.exit()