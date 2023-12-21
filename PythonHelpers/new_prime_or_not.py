

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

primes = []

not_primes = []

def algo(number_in_question):
    if number_in_question <= 2:
        # print(f"{number_in_question} is not prime")
        return False
    one_less = number_in_question - 1
    for digit in range(2, one_less):
        if number_in_question % digit == 0:
            return False
    else:
        primes.append(number)
        return True

for number in numbers:
    algo(number)

for number in primes:
    print(number)



''' for number in numbers:
        if number <= 2:
            print(f"{number} is not prime")
            return
        one_less = number - 1
        for digit in range(2, one_less):
            if number % digit == 0:
                return
        else:
            primes.append(number) '''