import datetime
import subprocess
import random
import re

# If the readline module is loaded, input will automatically inherit bash-like history-list editing
# (e.g. Control-P scrolls back to the last command, Control-N forward to the next one, Control-F moves the
# cursor to the right non-destructively, Control-B moves the cursor to the left non-destructively, etc.).
# Reference: https://docs.python.org/3/library/cmd.html
import readline
import string
import sqlite3
import sys
import os
import db

# TODO: Remove
#from listeners import http_callback_listener
from serpent_server import start_server
from cmd import Cmd

# Additional needs:
#
# 1.) Relays
# 2.) nmap integration / nmap query
# 3.) sqllite database for persisting results and configurations (logically segmented by op)
# 4.) Integrated target profiles (i.e. accumulation of data on found hosts, as well as a mechnism for accessing that data)
#

# References:
# https://docs.python.org/3/library/cmd.html
# https://wiki.python.org/moin/CmdModule
class SerpentShell(Cmd):
    # This is the directory where the serpent.py script is located
    SCRIPT_HOME_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
    
    # TODO: allow naming the file by the corresponding op / support file rotation
    OUTPUT_FILENAME = os.path.join(SCRIPT_HOME_DIRECTORY, 'serpent_trail.log')
    PAYLOADS_DIRECTORY = os.path.join(SCRIPT_HOME_DIRECTORY, 'payloads')

    # TODO: Add support for configuring all of these resources
    RESOURCE_TYPES = [ 'payloads', 'callbacks', 'profile' ]
    
    MAX_COMPLETIONS = 10
    CALLBACK_TOKEN_LENGTH = 64
    
    intro = 'Welcome to the serpent shell.   Type help or ? to list commands.\n'
    prompt = 'serpent> '
    file = None

    def __init__(self, current_op_id):
        super(SerpentShell, self).__init__()
        self.log_file = open(SerpentShell.OUTPUT_FILENAME, 'a+')
        self.current_op_id = current_op_id

    def random_string(self, length):
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))

    # TODO: Ensure that all do_* methods are integrated with this
    def log_command(self, command, results):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.log_file.write("[%s] %s%s\n" % (current_time, self.prompt, command))

        results_list = None
        if type(results) is list:
            results_list = results
        elif isinstance(results, str):
            results_list = results.split('\n')
        else:
            raise Exception("Unsupported results type '%s' encountered in the log_command() method" % type(results))
        
        for line in results_list:
            self.log_file.write("[%s] %s\n" % (current_time, line))

    # TODO: Uncomment if there is a performant way to do this (may just need to cache the list of available commands at start up, asynchronously ideally)
    # See https://stackoverflow.com/questions/187621/how-to-make-a-python-command-line-program-autocomplete-arbitrary-things-not-int/23959790
    # def complete_shell(self, text, line, start_index, end_index):
    #     if text != None:
    #         # See https://stackoverflow.com/questions/948008/linux-command-to-list-all-available-commands-and-aliases
    #         command = 'compgen -A function -abck %s' % text
    #         possible_system_commands = subprocess.check_output(command, shell=True, executable='/bin/bash').decode('utf-8').split('\n')

    #         if len(possible_system_commands) == 0:
    #             return [text]
    #         elif len(possible_system_commands) > SerpentShell.MAX_COMPLETIONS:
    #             return
    #         else:
    #             return possible_system_commands

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

    def command_usage_message(self, usage_msg):
        print('Error: incorrect command format\n')
        print('Usage: %s\n' % usage_msg)

    def complete_list(self, text, line, start_index, end_index):
        if text == None or len(text.strip()) == 0:
            return self.RESOURCE_TYPES
        else:
            return [ completion for completion in self.RESOURCE_TYPES if completion.startswith(text)]
        
    def do_list(self, arg):
        'List a set of resources [list <resource type>]'

        if len(arg.split(' ')) != 1:
            self.command_usage_message('list <resource type>')
        else:
            if arg == 'payloads':
                results = os.listdir(self.PAYLOADS_DIRECTORY)
                results_string = '\n'.join(results)
                self.log_command('list %s' % arg, results_string)
                print(results_string)
            else:
                print('Unknown resource type "%s"' % arg)

        print('')
    
    def find_payload(self, payload_name):
        payload_path = os.path.join(self.PAYLOADS_DIRECTORY, payload_name)

        if os.path.isfile(payload_path):
            return payload_path
        else:
            return None

    def do_query(self, arg):
        'Allows execution of arbitrary queries of the operational database; use with care [query <SQL statement>]'

        query = arg
        if re.compile('^show tables[\;]?$').match(arg):
            query = "select * from sqlite_master;"

        if not query.endswith(';'):
            query += ';'

        output = ''
        try:
            results = db.execute_query(query)
            output = '\n' + db.convert_results_to_string(results) + '\n'
        except sqlite3.OperationalError:
            output = '\nEncountered error while attempting to execute the provided query; please check your syntax and try again\n'

        print(output)
        self.log_command(arg, output)

    def do_configure(self, arg):
        # TODO: implement support for configuring the different payloads
        # and storing that configuration to refer back to when interacting
        # with the deployed agent; also need to dynamically configure the
        # listener hooks / C2 system
        pass

    def do_deploy(self, arg):
        'Deploy the specified payload to the specified target [deploy <payload> <target>]'

        args = arg.split(' ')
        if len(args) != 2:
            self.command_usage_message('deploy <payload> <target>')
        else:
            payload = args[0]
            target = args[1]
            payload_path = self.find_payload(payload)

            if payload_path == None:
                print("Payload '%s' not found" % arg)
            else:
                self.execute_shell_command('scp %s %s' % (payload_path, target))

    def do_connect(self, arg):
        # TODO: Support connecting to beacons (reverse shell type things)
        pass

    # TODO: Refactor / fix
    def do_listen(self, arg):
        'Start a callback listener with the given configuration (listen <callback type> <target> <destination port>)'

        args = arg.split(' ')
        if len(args) != 3:
            self.command_usage_message('listen <target> <destination port> <callback type>')
        else:
            pass
            # TODO: Cleanup / fix
            # callback_token = self.random_string(self.CALLBACK_TOKEN_LENGTH)
            # http_callback_listener.start_listener(self.current_op_id, args[0], callback_token, args[1], args[2])
            # db.record_agent_callback_configuration(self.current_op_id, args[0], callback_token, args[1], args[2])

    def do_send(self, arg):
        # TODO: Send message to specified agent
        pass

    def default(self, arg):
        self.execute_shell_command(arg)

    # TODO: Uncomment if there is a performant way to do this
    # def completedefault(self, text, line, start_index, end_index):
    #     self.complete_shell(text, line, start_index, end_index)
        
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
    db.create_db_tables_if_not_exists()
    current_op = db.get_current_op()

    # TODO: Pass in reference back to the main logic handler? (or integrate the web server with the database)
    start_server

    if current_op == None:
        db.start_op(input('Enter your operation name: '))

    current_op_id = current_op[0]
    SerpentShell(current_op_id).cmdloop()
