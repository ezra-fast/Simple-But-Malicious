# This is a template for the use of argparse in python, it is far from exhaustive

import argparse

parser = argparse.ArgumentParser(
    prog='cmdline_prime',
    description='Takes in a number from the command line and returns whether or not it is prime',
    epilog='Enter a number following the program name to check whether it is prime or not.')

parser.add_argument('filename')           # positional argument
parser.add_argument('-c', '--count')      # option that takes a value
parser.add_argument('-v', '--verbose', action='store_true')  # on/off flag

args = parser.parse_args()
print(args.filename, args.count, args.verbose)