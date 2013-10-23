'''
Standalone command line system for DOSE.

Date created: 22nd October 2013
'''
import os, sys, copy, random, readline, traceback
from datetime import datetime

import dose

def quotation():
    quotations = [
'''Touch a scientist and you touch a child.
  -- Ray Bradbury''',
'''There are no shortcuts in evolution.
  -- Louis D. Brandeis''',
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
'''Computer science is no more about computers than astronomy is about telescopes.
  -- Edsger Dijkstra''',
'''Only two things are infinite, the universe and human stupidity, 
and I'm not sure about the former.
  -- Albert Einstein''',
'''No amount of experimentation can ever prove me right; 
a single experiment can prove me wrong.
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
'''Science has proof without any certainty. 
Creationists have certainty without any proof.
  -- Ashley Montague''',
'''Anyone who attempts to generate random numbers by deterministic means is, 
of course, living in a state of sin.
  -- John von Neumann'''
'''To me there has never been a higher source of earthly honor or distinction 
than that connected with advances in science.
  -- Isaac Newton''',
'''If I have seen further than others, 
it is by standing upon the shoulders of giants.
  -- Isaac Newton'''
'''If you cannot - in the long run - tell everyone what you have been doing, 
your doing has been worthless.
  -- Erwin Schrodinger''']
    return random.choice(quotations)

class DOSECommandShell(object):
    
    commands = ('connectdb',
                'copyright', 
                'credits',
                'help', 
                'license',
                'show',)
    
    def __init__(self):
        self.history = {}
        self.results = {}
        self.environment = {'cwd': os.getcwd(),
                            'starting_time': str(datetime.utcnow()),
                            'terminate_shell': 'quit'}
        
    def header(self):
        print '''
Digital Organisms Simulation Environment (DOSE), version 0.1
Current time is %s

%s

Type "help", "copyright", "credits" or "license" for more information.
To exit this application, type "quit".
''' % (self.environment['starting_time'], quotation())
    
    def do_connectdb(self, arg, count): pass
    def help_connectdb(self):
        print
        print
        print
        
    def do_copyright(self, arg, count):
        print 
        print "Copyright 2010-2013, Maurice HT Ling (on behalf of all authors)"
        print
    
    def do_credits(self, arg, count):
        print
        print '''DOSE Project Team
Project architect: Maurice HT Ling (mauriceling@acm.org)
Lead developer: Clarence Castillo'''
        print
    
    def do_help(self, arg, count):
        if arg == '':
            print
            print '''List of available commands:
connectdb           copyright           credits          help    
license             quit                show

Type help <command> for more help (if any)'''
            print
        elif arg == 'quit': self.help_quit()
        elif arg == 'show': self.help_show()
    
    def do_license(self, arg, count):
        print
        print '''
Unless otherwise specified, all files in dose/copads folder will be licensed 
under Python Software Foundation License version 2.
All other files, including DOSE, will be GNU General Public License version 3.
        '''
        print
    
    def do_quit(self, arg, count):
        print
        print '''Are you going off?? -:(
Please contact Maurice Ling (mauriceling@acm.org) if you need any help.
Goodbye! Have a nice day and hope to see you again soon!

%s

Current time is %s''' % (quotation(), str(datetime.utcnow()))
        print
    
    def help_quit(self):
        print '''
Command: quit
Description: Terminate this application'''
        print
    
    def do_show(self, arg, count):
        if arg == 'environment':
            self.results[count] = copy.deepcopy(self.environment)
            print 'Environment variables:'
            for key in self.environment.keys():
                print key, '=', self.environment[key]
        elif arg == 'history':
            self.results[count] = copy.deepcopy(self.history)
            keys = self.history.keys()
            keys.sort()
            for k in keys:
                print 'Count =', k, '| Command =', self.history[k]
        elif arg.startswith('history') and arg[-1] != 'y':
            arg = [str(x.strip()) for x in arg.split(' ')]
            if len(arg) > 1:
                self.results[count] = self.history[str(arg[1])]
                print 'Count =', arg[1], '| Command =', self.history[str(arg[1])]
                
    def help_show(self):
        print '''
Command: show <options>
    <options> = {environment | history | history <item>}
Description: Display internal variables

<options> = environment
    Display all environmental variables in DOSE command shell as one line 
    per environmental variable.
<options> = history
    Display all history in the current session, in the format of 
    Command = <command number> | Command = <command string>
<options> = history <item>
    Display only specific historical command, where <item> is the command 
    number'''
        print
            
    def command_handler(self, cmd, arg, count):
        if cmd == 'connectdb': self.do_connectdb(arg, count)
        if cmd == 'copyright': self.do_copyright(arg, count)
        if cmd == 'credits': self.do_credits(arg, count)
        if cmd == 'help': self.do_help(arg, count)
        if cmd == 'license': self.do_license(arg, count)
        if cmd == 'show': self.do_show(arg, count)
        
    def cmdloop(self):
        statement = ''
        count = 1
        while True:
            try:
                statement = raw_input("DOSE:%s > " % str(count))
                statement = str(statement.strip())
                statement = statement.lower()
                self.history[str(count)] = statement
                cmd = statement.split(' ')[0]
                arg = ' '.join(statement.split(' ')[1:])
                arg = arg.strip()
                if cmd in self.commands:
                    self.command_handler(cmd, arg, count)
                elif cmd == 'quit':
                    self.do_quit(arg, count)
                    break
                else:
                    error_message = cmd + ' is not a valid command.'
                    self.history[str(count)] = self.history[str(count)] + \
                        ' | Error message: ' + error_message
                    print error_message
                count = count + 1
            except:
                error_message = list(self.formatExceptionInfo())
                self.results[str(count)] = error_message
                for line in error_message:
                    if (type(line) == list):
                        for l in line: print l
                    print line
            
    def completer(self, text, state):
        options = [x for x in self.commands 
                   if x.startswith(text)]
        try:
            return options[state]
        except IndexError:
            return None
        
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
    readline.set_completer(shell.completer)     # enables autocompletion
    readline.parse_and_bind("tab: complete")
    shell.cmdloop()
    sys.exit()