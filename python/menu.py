'''
This script acts as a wrapper to display the current Euler solutions
and allows the user to select one to run.

Full problem list can be found at https://projecteuler.net/problems
--> When logged in there are PDF solutions discussing the mathematics
    behind each problem once you have submitted a valid solution.

TODO:
~~~~~
>   Add search functionality for users to locate programs based on
    docstring contents.
>   List in batches: 20 per batch?
>   Pre-generate search fields based on most commonly used words in
    the located docstrings.
'''
import os
from importlib import import_module


def main():
    # -- Define known files in the directory [including this file!] that should be excluded
    excludes = ['menu.py', 'euler.py', 'eulerXX.py']
    # -- List all of the current .py files in the directory and order them.
    pyFiles = [f for f in os.listdir('.') if os.path.isfile(f) if f[-3:] == '.py']
    # -- Remove the unwanted files from the list.
    for unwanted in excludes:
        if unwanted in pyFiles:
            pyFiles.remove(unwanted)
    pyFiles.sort(key=lambda f: int(f[5:-3]))
    os.system('clear')
    print("This program is a wrapper for I.Morrison's work on ProjectEuler.net")
    print('The following programs are available::\n')
    # -- Print the file names and related docstrings to StdOut
    for p in pyFiles:
        f = import_module(p[:-3])
        print(p[:-3], '--> ', f.__doc__)
    choice = input('\nEnter the program name you wish to run:\n--> ')
    # -- rebuild full file name and spawn a shell process to run the script
    run = 'python ' + choice + '.py'
    os.system(run)

if __name__ == '__main__':
    main()
