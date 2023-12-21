# this code works

def string_reverser(string):
    retlist = []
    for letter in range(len(string) - 1, -1, -1):
        retlist.append(string[letter])
    return retlist

def list_printer(word):
    print("Reversed: ", end='')
    for letter in word:
        print(letter, end='')

samlist = []

string = input("Please enter a word: ")

samlist = string_reverser(string)

list_printer(samlist)