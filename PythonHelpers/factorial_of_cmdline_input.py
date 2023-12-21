'''This script works to take in a number as command line input and calculate the factorial thereof.'''
import sys
def calculator(number):
    answer = number
    for i in range(number - 1, 0, -1):
        answer = answer * i
    return answer
def factorial_of_input():
    args = sys.argv
    if (len(args) != 2):
        print("Incorrect Usage.\nUsage: python program.py (number)")
        exit()
    number = int(args[1])
    print(f"The factorial of {number} is: {calculator(number)}")
def main():
    factorial_of_input()
main()