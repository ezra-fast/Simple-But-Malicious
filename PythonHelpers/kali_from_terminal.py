''' This script will open a virtualbox VM on Ubuntu based on the name of the VM given as argument 1. It should be made into the alias 'redONE', 'windows10', 'blueNINE', etc. '''

# This script can be added onto so that the network adapter can be configured programmatically.

import subprocess
import argparse

def parsing_the_VM_name():
    parser = argparse.ArgumentParser(
    add_help=False,
    prog='VM_from_terminal',
    description='Launch VMs by alias from terminal in Ubuntu',
    epilog='This script should setup as an alias in Ubuntu, wherein it is invoked with the name of the VM to be launched as the first command line argument')

    parser.add_argument('machine_name')           # positional argument
    parser.add_argument('h', '--help', action='store_true')             # false by default; if true, it will print VMs in VirtualBox

    args = parser.parse_args()          # accessible via args.object1, args.object2, etc.
    return args

def start_the_machine(arguments):
    machine_name = arguments.machine_name
    if (arguments.help == True):
        nineelevenwasaninsidejob = subprocess.run(['VBoxManage', 'list', 'vms'], capture_output=True, text=True)
        print(f'Possible Machines:\n\n{nineelevenwasaninsidejob.stdout}')
        exit(0)
    try:
        machines = ['redONE', 'windows10', 'blueNINE']                  # List of VMs
        if (machine_name not in machines):
            print('INVALID MACHINE')
            exit(-1)
        the_command = ['VBoxManage', '-q', 'startvm', machine_name]
        subprocess.run(the_command, check=True)
    except subprocess.CalledProcessError as error:
        print(f'Could not start {machine_name};\nThe error raised: {error}')

def main():
    start_the_machine(parsing_the_VM_name())
if __name__ == '__main__':
    main()