'''this code works to populate two lists and find the common elements'''
from random import randint
def find_common_between_lists(one, two):
    commonalities = []
    for item in one:
        if item in two and item in one:
            commonalities.append(item)
    return commonalities
def list_populator(one, two):
    for i in range(1, 20):
        one.append(randint(0, 30))
        two.append(randint(0, 45))
    print(f"List 1: {one}\nList 2: {two}")
one = []
two = []
list_populator(one, two)
commonalities = find_common_between_lists(one, two)
print(f"Common to both: {commonalities}")