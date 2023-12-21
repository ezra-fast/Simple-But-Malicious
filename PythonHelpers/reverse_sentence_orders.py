'''This script works to take in a sentence from the user and reverse the order thereof.'''
def sentence_gatherer():
    sentence = input("Enter the sentence you want reversed: ")
    sentence = sentence.split()
    return sentence
def sentence_order_reverser(list_of_words):
    for i in range(len(list_of_words) - 1, -1, -1):
        print(f"{list_of_words[i]} ", end='')
def main():
    sentence = sentence_gatherer()
    sentence_order_reverser(sentence)
    exit()
main()