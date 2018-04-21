import datetime
import subprocess
import sys
import os

from cmd import Cmd

# References:
# https://docs.python.org/3/library/cmd.html
# https://wiki.python.org/moin/CmdModule
class SerpentShell(Cmd):
    # This is the directory where the serpent.py script is located
    SCRIPT_HOME_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    
    # TODO: allow naming the file by the corresponding op / support file rotation
    OUTPUT_FILENAME = os.path.join(SCRIPT_HOME_DIRECTORY, 'serpent_trail.log')
    PAYLOADS_DIRECTORY = os.path.join(SCRIPT_HOME_DIRECTORY, 'payloads')

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

    def execute_shell_command(self, command):
        # TODO: Implement graceful scrolling over long results
        try:
            result = subprocess.check_output(command.split(' ')).decode('utf-8')
            self.log_command(command, result)
            print("%s" % result)
        except:
            print(sys.exc_info())
            print('Exception encountered while attempting to execute shell command "%s"' % command)

    # TODO: Get this to work more seemlessly;
    # "shell bash" works when running; just need to grab STDOUT from the subprocess and feed the appropriate values to STDIN
    def do_shell(self, arg):
        'Execute a shell command'

        self.execute_shell_command(arg)
            
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

    def find_payload(self, payload_name):
        payload_path = os.path.join(self.PAYLOADS_DIRECTORY, payload_name)

        if os.path.isfile(payload_path):
            return payload_path
        else:
            return None

    # TODO: Add a list_payloads action
    def do_deploy(self, arg):
        'Deploy the specified payload to the specified target [deploy <payload> <target>]'

        args = arg.split(' ')
        if len(args) != 2:
            print('Error: incorrect command format\n')
            print('Usage: deploy <payload> <target>\n')
        else:
            payload = args[0]
            target = args[1]
            payload_path = self.find_payload(payload)

            if payload_path == None:
                print("Payload '%s' not found" % arg)
            else:
                self.execute_shell_command('scp %s %s' % (payload_path, target))

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
