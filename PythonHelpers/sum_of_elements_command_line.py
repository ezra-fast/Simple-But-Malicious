'''This script works to take in numbers from cmd, print program banner, and print the sum of the inputs'''
import pyfiglet
import sys
def command_input():
    if (len(sys.argv[1:]) < 2):
        print("Please specify numbers as command line input.\nThey will be added together.")
        exit()
    cmd_args = sys.argv[1:]
    return cmd_args
def figlet():
    text = "Sum of Elements"
    font = "standard"  
    banner = pyfiglet.figlet_format(text, font=font)
    print(banner)
def sum_of_args(args):
    sum = 0
    for number in args:
        sum += int(number)
    return sum
def main():
    command_input()
    figlet()
    print(f"The sum of the inputs is: {sum_of_args(command_input())}")
main()