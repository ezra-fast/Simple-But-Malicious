'''This code works to take a word as input on the command line and check if that word is a palindrome'''
import sys
def argument_checker():
    if (len(sys.argv) != 2):
        print("Incorrect Usage.\nSpecify the string you would like to check as a command line argument")
        exit()
def palindrome_checker(word):
    reversed = []
    for letter in range(len(word) - 1, -1, -1):
        reversed.append(word[letter])
    if (list_vs_string_comparison(reversed, word)):
        print(f"{word} is a palindrome")
        return True
    else:
        print(f"{word} is not a palindrome.")
        return False
def list_vs_string_comparison(list, string):
    string_list = []
    for character in string:
        string_list.append(character)
    for letter in range(0, len(list)):
        if (list[letter] != string_list[letter]):
            return False
    return True
def main():
    argument_checker()
    word = sys.argv[1]
    palindrome_checker(word)
main()