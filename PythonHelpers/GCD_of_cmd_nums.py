'''This code works to take in two numbers as command line input and calculate the GCD thereof.'''
import sys
def input_from_cmd():
    if (len(sys.argv) != 3):
        print("Incorrect Usage.\nEnter two numbers as command line arguments.")
        exit()
def greatest_common_divisor():
    one = int(sys.argv[1])
    two = int(sys.argv[2])
    smaller = 0
    largest = 0
    list_of_divisors = []
    if (one <= two):
        smaller = one
    else:
        smaller = two
    for i in range(1, smaller):
        if (one % i == 0 and two % i == 0):
            list_of_divisors.append(i)
    for number in range(0, len(list_of_divisors)):
        if list_of_divisors[number] > largest:
            largest = list_of_divisors[number]
            print(largest)
    return largest
def main():
    input_from_cmd()
    largest = greatest_common_divisor()
    print(f"The GCD of {sys.argv[1]} and {sys.argv[2]} is: {largest}")
main()