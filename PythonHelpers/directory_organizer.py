''' This script will organize the input directory by creating sub directories and putting similar files types 
    in their respective subdirectories'''

import argparse
import os
import pathlib
import shutil

def argument_grabber():
    parser = argparse.ArgumentParser(
        prog='dir_organizer',
        description='Takes in a directory to organize and places files into unique subdirectories based on file type.',
        epilog='Enter a directory to organize.')

    parser.add_argument('directory')           # positional argument

    prelim_args = parser.parse_args()
    arg = []
    arg.append(prelim_args.directory)
    return arg

def organize_dir(dir):
    for file in os.listdir(dir):
        file_extension = pathlib.Path(file).suffix
        if file_extension == '':
            pass
        else:
            # print(file_extension.replace('.', ''))
            if not os.path.isdir(f"{dir}\\{file_extension.replace('.', '')}_files"):
                os.mkdir(f"{dir}\\{file_extension.replace('.', '')}_files")
            shutil.move(f'{dir}\\{file}', f"{dir}\\{file_extension.replace('.', '')}_files")
            print(f"{file} moved to {dir}\\{file_extension.replace('.', '')}_files")

directory = argument_grabber()
organize_dir(directory[0])