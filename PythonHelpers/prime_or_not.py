import math

numbers = [3, 4, 5, 6, 7, 8, 9, 10]
primes = []

def algorithm(number):
    if number < 2:
        return
    one_less = number - 1
    for i in range(2, one_less):   # the counter increments
        # print(i)
        i = i + 1
        if number % i == 0 and number != i:
            break
        else:
            primes.append(number)

for digit in numbers:
    algorithm(digit)

for number in primes:
    print(number)