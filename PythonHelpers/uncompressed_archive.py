''' This python script takes a directory as input and creates an uncompressed archive thereof.
    The directory input must be a full path and the archive will be placed in the dir that the script is invoked in. '''

import shutil       # use shutil.make_archive --> creates uncompressed .ZIP file; mainly used for organizing multiple files into a single file
import argparse
import os

def argument_grabber():
    parser = argparse.ArgumentParser(
        prog='uncompressed_archiver',
        description='Takes in a directory and creates an uncompressed archive in the current directory.',
        epilog='Provide a full directory path to archive.')

    parser.add_argument('dir')           # positional argument

    prelim_args = parser.parse_args()

    args = []

    args.append(prelim_args.dir)

    return args

def archiver(dir):
    destination = '.\\uncompressed_archive'
    archive = shutil.make_archive(destination , 'zip', dir)     # main functional line right here
    if not os.path.exists(f'{destination}.zip'):
        print('Error creating .zip file.')
        exit(-1)
    print(f'Archive: {archive}')
    return archive

def main():
    args = argument_grabber()
    archiver(args[0])

main()