# This code works to continuously find the factorial of inputted numbers
def factorial_finder():
    number = int(input("Please enter a number: "))
    answer = number
    for i in range(number - 1, 0, -1):
        answer = answer * i
    print(f"The factorial of {number} is {answer}")
    return True
while 1:
    try:
        factorial_finder()
    except:
        if KeyboardInterrupt:
            exit()