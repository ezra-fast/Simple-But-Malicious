'''This program works to take in a number from cmd with the -n option,
    and calculates whether or not that number is prime.'''
import argparse
def prime_checker(number):
    for i in range(2, number - 1):
        if (number % i == 0):
            print(f"{number} is not prime number.")
            exit()
        else:
            print(f"{number} is a prime number")
            exit()
def professional_parser():
    parser = argparse.ArgumentParser(
        prog='cmdline_prime',
        description='Takes in a number from the command line and returns whether or not it is prime',
        epilog='Enter a number following the program name to check whether it is prime or not.')
    parser.add_argument('-n', '--number', required=True)
    args = parser.parse_args()
    return args
def main():
    args = professional_parser()
    prime_checker(int(args.number))
main()