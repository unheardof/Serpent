import datetime
import subprocess
import sys
from cmd import Cmd

# References:
# https://docs.python.org/3/library/cmd.html
# https://wiki.python.org/moin/CmdModule
class SerpentShell(Cmd):
    # TODO: protect against overwritting
    # TODO: allow tagging / naming the file by ops
    # TODO: support file rotation
    # TODO: prepend date-time to each line before writing it to the log
    OUTPUT_FILENAME = './serpent_trail.log'

    MAX_COMPLETIONS = 10
    
    intro = 'Welcome to the serpent shell.   Type help or ? to list commands.\n'
    prompt = '(serpent) '
    file = None

    def __init__(self):
        super(SerpentShell, self).__init__()
        self.log_file = open(SerpentShell.OUTPUT_FILENAME, 'a+')

    def log_command(self, command, results):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.log_file.write("[%s] > %s\n" % (current_time, command))
        for line in results.split('\n'):
            self.log_file.write("[%s] %s\n" % (current_time, line))

    # TODO: get this working
    # See https://stackoverflow.com/questions/187621/how-to-make-a-python-command-line-program-autocomplete-arbitrary-things-not-int/23959790
    def complete_shell(self, text, line, start_index, end_index):
        if text:
            # See https://stackoverflow.com/questions/948008/linux-command-to-list-all-available-commands-and-aliases
            possible_system_commands = subprocess.check_output('compgen -A function -abck %s' % text, shell=True, executable='/bin/bash')

            if len(possible_system_commands) == 0:
                return [text]
            elif len(possible_system_commands) > SerpentShell.MAX_COMPLETIONS:
                return ["%d possiblities"] % (len(possible_system_commands))
            else:
                return possible_system_commands

    # TODO: Get this to work more seemlessly;
    # "shell bash" works when running; just need to grab STDOUT from the subprocess and feed the appropriate values to STDIN
    def do_shell(self, arg):
        'Execute a shell command'

        # TODO: Implement graceful scrolling over long results
        try:
            result = subprocess.check_output(arg.split(' ')).decode('utf-8')
            self.log_command(arg, result)
            print("%s" % result)
        except:
            print(sys.exc_info())
            print('Exception encountered while attempting to execute shell command "%s"' % arg)
            
    def do_load(self, arg):
        'Load a given module'
        print('Would have loaded %s' % arg)
        #self.log_command(arg, result)
        #print("%s" % result)

    # TODO: Implement
    # def do_(self, arg):
    #     pass

    # def do_(self, arg):
    #     pass

    # def do_(self, arg):
    #     pass

    def do_quit(self, arg):
        'Stop recording, close the serpent window, and exit'
        print('Thank you for using Serpent')
        self.close()
        return True

    def close(self):
        if self.log_file:
            self.log_file.close()
            self.log_file = None
            
if __name__ == '__main__':
    SerpentShell().cmdloop()
