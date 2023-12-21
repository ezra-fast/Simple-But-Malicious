''' This script finds the MD5 hash of input material and prints it to the console '''

import hashlib
import argparse

def arguments():
    parser = argparse.ArgumentParser(
        prog='MD5_Hasher',
        description='Takes file and calculates the MD5 hash thereof; prints results to the console',
        epilog='Provide a file to find the MD5 hash thereof.')

    parser.add_argument('file')

    prelim_args = parser.parse_args()
    args = []
    args.append(prelim_args.file)
    return args

def MD5_hash_finder(material):
    with open(material, 'rb') as file:
        data = file.read()
    h_object = hashlib.md5()
    h_object.update(data)
    md5_hash = h_object.hexdigest()
    return md5_hash

def main():
    args = arguments()
    material = args[0]
    hash = MD5_hash_finder(material)
    print(f'\nThe MD5 Hash: {hash}\n')

main()