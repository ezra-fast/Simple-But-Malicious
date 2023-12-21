''' This script takes in a full directory path as input and creates a compressed archive thereof in the dir that the script was invoked from. '''

import zipfile       # Create a ZipFile object; use the write() method of the object to write each file in the object to the destination archive
import argparse
import os

def argument_grabber():
    parser = argparse.ArgumentParser(
        prog='uncompressed_archiver',
        description='Takes in a directory and creates a compressed archive in the current directory.',
        epilog='Provide a full directory path to compress and archive. DO NOT CONCLUDE THE PATH WITH \\')

    parser.add_argument('dir')           # positional argument

    prelim_args = parser.parse_args()

    args = []

    args.append(prelim_args.dir)

    return args

def compressed_archiver(dir):
    destination = '.\\compressed_archive.zip'

    with zipfile.ZipFile(destination, 'w') as zipfile_object:
        for material in os.listdir(dir):
            zipfile_object.write(f'{dir}\\{material}')
    
    if not os.path.exists(f'{destination}'):
        print(f'Error creating compressed archive: {destination}.zip')
        exit(-1)
    print(f'Compressed Archive: {destination}')

def main():
    args = argument_grabber()
    compressed_archiver(args[0])

main()