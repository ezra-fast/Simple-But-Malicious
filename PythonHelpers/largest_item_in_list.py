import random # This code works
def random_populator(list):
    for i in range(0, 60):
        number = random.randint(0, 4000)
        list.append(number)
    return list
def largest_finder(list):
    current = list[0]
    for item in list:
        if item > current:
            current = item
    return current
list = []
list = random_populator(list)
print(f"The biggest value is: {largest_finder(list)}")