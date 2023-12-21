'''This code works to generate a list of random numbers and find the median
value thereof'''
from random import randint
def list_populator(list):
    length = int(input("Enter the length of the list: "))
    i = 0
    while (i < length):
        list.append(randint(1, 30))
        i += 1
def sort_ascending():
    list = []
    list_populator(list)
    for item in range(0, len(list), 1):     # offsets are accessible with 'item'
        min_index = item
        for value in range(min_index, len(list), 1):    # value is the lowest unsorted offset
            if list[value] < list[min_index]:
                holder = list[min_index]
                list[min_index] = list[value]
                list[value] = holder
    return list
def median_finder(list):
    if (len(list) % 2 == 1):    # if the number of list items is odd
        middle = int((len(list) / 2) + 0.5)
        print(f"The median value of the list is: {list[middle]}")
        print("The list: ", end='')
        [print(f"{value} ", end='') for value in list]
    elif (len(list) % 2 == 0):
        upper_middle = len(list) / 2
        lower_middle = upper_middle - 1
        median = (list[int(upper_middle)] + list[int(lower_middle)]) / 2
        print(f"The median value of the list is: {median}")
        print("The list: ", end='')
        [print(f"{value} ", end='') for value in list]
list = sort_ascending()
median_finder(list)