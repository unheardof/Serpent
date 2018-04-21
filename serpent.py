from cmd import Cmd

# Refernce: https://docs.python.org/3/library/cmd.html

class SerpentShell(Cmd):
    intro = 'Welcome to the turtle shell.   Type help or ? to list commands.\n'
    prompt = '(serpent) '
    file = None # TODO: Save to a default file location (and protect against file overwritting)
    
    def __init__(self):
        pass

    def do_load(self, arg):
        'Load a given module'
        print('Would have loaded %s' % arg)

    # TODO: Implement
    # def do_(self, arg):
    #     pass

    # def do_(self, arg):
    #     pass

    # def do_(self, arg):
    #     pass

    def do_record(self, arg):
        'Save future commands to filename:  RECORD rose.cmd'
        self.file = open(arg, 'w')

     def do_quit(self, arg):
        'Stop recording, close the serpent window, and exit'
        print('Thank you for using Serpent')
        self.close()
        bye()
        return True

    def close(self):
        if self.file:
            self.file.close()
            self.file = None
            
if __name__ == '__main__':
    SerpentShell().cmdloop()
