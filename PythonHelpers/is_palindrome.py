# This code works

def check_if_palindrome(word):
    list_string = []
    for letter in word:
        list_string.append(letter.lower())
    length = len(word) - 1
    offset = 0
    while (offset < len(word) / 2):
        if list_string[offset] != list_string[length - offset]:
            print(f"{word} is not a Palindrome")
            return
        offset += 1
    print(f"{word} is a Palindrome")
    return True
word = input("Enter a word: ")
check_if_palindrome(word)