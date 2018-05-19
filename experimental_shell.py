import subprocess

def execute_bash_shell():
    process = subprocess.Popen(['/bin/sh'], stdout=subprocess.PIPE)

    while True:
        out = process.stdout.readline()
        print(out.decode('utf-8'))

while True:
    user_input = input("serpent> ")
    


