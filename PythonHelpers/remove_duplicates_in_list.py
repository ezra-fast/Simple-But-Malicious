'''This code works to populate 2 lists randomly and remove any duplicate
numbers so that the lists are unique'''
from random import randint
def find_and_remove_duplicates(list1, list2):
    in_both = []
    for item in list1:
        if item in list2 and item in list1:
            in_both.append(item)
    for item in list2:
        if item in list2 and item in list1 and item not in in_both:
            in_both.append(item)
    print(f"In Both: {in_both}")
    for item in in_both:
        if item in list1 and item in list2:
            list1.remove(item)
            list2.remove(item)
def list_populator(list):
    for i in range(1, 10, 1):
        list.append(randint(0, 20))
    return list
list_1 = []
list_2 = []
list_1 = list_populator(list_1)
list_2 = list_populator(list_2)
print(f"{list_1}")
print(f"{list_2}")
find_and_remove_duplicates(list_1, list_2)
print(f"{list_1}")
print(f"{list_2}")