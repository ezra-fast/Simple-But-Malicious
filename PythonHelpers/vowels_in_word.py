# This code works
def vowels_in_string(word):
    vowel_counter = 0
    list = []
    vowels = ['a', 'e', 'i', 'o', 'u', 'y']
    for letters in word:
        list.append(letters)
    for letters in list:
        if letters in vowels:
            vowel_counter += 1
    return vowel_counter
word = input("Please enter a string: ")
number_of_vowels = vowels_in_string(word)
if (number_of_vowels == 1):
    print(f"There is {number_of_vowels} vowel in {word}")
elif (number_of_vowels < 1):
    print(f"There are no vowels in {word}")
elif (number_of_vowels > 1):
    print(f"There are {number_of_vowels} vowels in {word}")