# This code works to see if two strings are anagrams
def anagram_finder():
    word = input("Please enter the first word: ")
    string = input("Please enter the second word: ")    
    word_list = []
    string_list = []
    for letter in word:
        word_list.append(letter)
    for letter in string:
        string_list.append(letter)
    for letter in word_list: 
        if letter not in string_list:
            print("The two inputs are not anagrams.")
            return False
    print("The two inputs are anagrams.")
    return True
anagram_finder()