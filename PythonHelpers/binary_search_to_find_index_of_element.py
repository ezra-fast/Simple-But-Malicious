''' This code works to populate and sort a list, and then use a binary chop to locate the offset of a number the user wishes to search for'''
''' Error Handling:
    1. if the number not in list --> handled by appending the number automatically before populating and sorting the list'''
import random
def list_sorter(list):
    for i in range(len(list)):
        min_index = i
        for y in range(min_index, len(list), 1):
            if list[y] < list[min_index]:
                holder = list[y]
                list[y] = list[min_index]
                list[min_index] = holder
    return list
def binary_search_for_element(number, list):
    high = len(list) - 1    # This is the last index position at the outset
    low = 0
    while low <= high:
        middle = (high + low) // 2
        if number < list[middle]:
            high = middle
        elif number > list[middle]:
            low = middle
        elif number == list[middle]:
            return middle 
    return middle
def list_populator(list, number):
    list.append(number)
    list_size = int(input("Enter the size of the list: "))
    list_range = int(input("Enter the numerical range of the list: "))
    for i in range(list_size):
        list.append(random.randint(0, list_range))
def main():
    sample = [250]
    number = int(input("Enter the number you want to find: "))
    list_populator(sample, number)
    list_sorter(sample)
    offset_of_number = binary_search_for_element(number, sample)
    print(f"The List: {sample}\nThe Offset: {offset_of_number} - (Item number {offset_of_number + 1} in the list.)")
main()