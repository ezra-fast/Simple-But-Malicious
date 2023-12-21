# This code works

def sum_of_list(list):
    result = 0
    element = list[-1]
    while (element != 0):
        result = result + element
        element = element - 1
    return result
def populate_list(number, list):
    for i in range(number):
        list.append(i + 1)
    return list
the_list = []
input = int(input("Enter the number of list items: "))
the_list = populate_list(input, the_list)
print(f"The sum of the list is: {sum_of_list(the_list)}")