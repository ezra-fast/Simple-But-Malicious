# This code works
import random
def second_largest(list):
    biggest = list[0]
    second_biggest = list[0]
    for number in range(0, len(list), 1):
        if list[number] > biggest:
            biggest = list[number]
    for number in range(0, len(list), 1):
        if list[number] > second_biggest and list[number] < biggest:
            second_biggest = list[number]
    return second_biggest
def largest_in_list(list):
    biggest = list[0]
    for number in range(0, len(list), 1):
        if list[number] > biggest:
            biggest = list[number]
    return biggest
def list_populator():
    list = []
    for i in range(1, 100):
        list.append(random.randint(1, 1000))
    return list
list_1 = []
list_1 = list_populator()
second_biggest = second_largest(list_1)
first_biggest = largest_in_list(list_1)
if (second_biggest != first_biggest):
    print(f"First largest: {first_biggest}")
    print(f"Second largest: {second_biggest}")
else:
    print("Error in Populating the List with Random Numbers.")