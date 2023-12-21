'''This code works to generate a list and find the largest possible sum between 2 list items.'''
import random
def list_populator(the_list):
    # the_list = []
    list_size = int(input("Enter the size of the list: "))
    list_range = int(input("Enter the numerical range of the list: "))
    for g in range(list_size):
        the_list.append(random.randint(0, list_range))
    return list
def largest_sum_finder(list):
    largest = 0
    current_sum = 0
    for i in range(len(list)):
        for h in range(len(list)):
            if (i != h):
                current_sum = list[i] + list[h]
            if (current_sum > largest):
                largest = current_sum
                first = list[i]
                second = list[h]
    print(f"\nThe list: {list}\n\nThe largest sum of any two values in the list is: {largest}\n\nThe two numbers are: {first} and {second}")
    return largest
def main():
    the_list = []
    list_populator(the_list)
    largest_sum_finder(the_list)
main()