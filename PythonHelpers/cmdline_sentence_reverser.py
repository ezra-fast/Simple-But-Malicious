import argparse

def sentence_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sentence', nargs='+', help='Please enter a sentence.', required=True)
    args = parser.parse_args()
    sentence = ' '.join(args.sentence)
    return sentence

def reverse_the_order(sentence):
    for letter in range()

def main():
    sentence = sentence_from_args()
    reverse_the_order(sentence)
main()