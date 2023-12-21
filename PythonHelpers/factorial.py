# This code works

def factorial_calculator(number):
    result = 1
    for i in range(1, number):
        result = result * number
        number = number - 1
    return result

number = int(input("Please enter a Number: "))

factorial = factorial_calculator(number)

print(factorial)