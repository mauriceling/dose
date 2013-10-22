'''
Standalone command line system for DOSE.

Date created: 22nd October 2013
'''
import os, sys
from datetime import datetime
import dose

class DOSECommandShell(object):
    
    commands = ('copyright', 
                'credits',
                'help', 
                'license',
                'quit')
    
    def __init__(self):
        self.history = {}
        self.data = {}
        self.environment = {'starting_time': str(datetime.utcnow()),
                            'terminate_shell': 'quit'}
        
    def header(self):
        print '''
Digital Organisms Simulation Environment (DOSE), version 1.0
Current time is %s
Type "help", "copyright", "credits" or "license" for more information.
To exit this application, type "quit".
        ''' % self.environment['starting_time']
    
    def do_copyright(self, cmd, arg, count):
        print 
        print "Copyright 2010-2013, Maurice HT Ling (on behalf of all authors)"
        print
    
    def do_credits(self, cmd, arg, count):
        pass
    
    def do_help(self, cmd, arg, count):
        if arg == '':
            print
            print '''List of available commands:
copyright    credits    help    license    quit

Type help <command> for more help (if any)'''
            print
        elif arg == 'quit': self.help_quit()
    
    def do_license(self, cmd, arg, count):
        print
        print '''
Unless otherwise specified, all files in dose/copads folder will be licensed 
under Python Software Foundation License version 2.
All other files, including DOSE, will be GNU General Public License version 3.
        '''
        print
    
    def do_quit(self, cmd, arg, count):
        print
        print '''You are going off?? -:(
Please contact Maurice Ling (mauriceling@acm.org) if you need any help.
Goodbye! Hope to see you again soon!
Current time is %s''' % str(datetime.utcnow())
        sys.exit()
    
    def help_quit(self):
        print '''
Command: quit
Description: Terminate this application'''
        print
        
    def command_handler(self, cmd, arg, count):
        if cmd == 'copyright': self.do_copyright(cmd, arg, count)
        if cmd == 'credits': self.do_credits(cmd, arg, count)
        if cmd == 'help': self.do_help(cmd, arg, count)
        if cmd == 'license': self.do_license(cmd, arg, count)
        if cmd == 'quit': self.do_quit(cmd, arg, count)
        
    def cmdloop(self):
        statement = ''
        while True:
            count = 1
            statement = raw_input("DOSE:%s > " % str(count))
            statement = str(statement.strip())
            statement = statement.lower()
            self.history[str(count)] = statement
            cmd = statement.split(' ')[0]
            arg = ' '.join(statement.split(' ')[1:])
            if cmd in self.commands:
                self.command_handler(cmd, arg, count)
            else:
                error_message = cmd + ' is not a valid command.'
                self.history[str(count)] = self.history[str(count)] + \
                    ' Error message: [' + error_message + ']'
                print error_message
            count = count + 1
            
            
if __name__ == '__main__':
    shell = DOSECommandShell()
    shell.header()
    shell.cmdloop()