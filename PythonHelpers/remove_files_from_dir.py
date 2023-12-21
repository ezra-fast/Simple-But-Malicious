# This script will traverse the sub-tree of the specified directory and remove any files in the list of files provided

import os
import sys

def list_maker():
    with open(sys.argv[1], 'r') as file:
        files = file.read()
    file_names = files.split('\n')
    file_names = [filename.strip() for filename in file_names]
    # print(file_names)
    return file_names

def remove_files_from_dir(dir, names):                     # recursive function working for once :()
    # dir = sys.argv[2]
    for name in os.listdir(dir):
        if (os.path.isdir(f'{dir}\\{name}') == True):
            remove_files_from_dir(f'{dir}\\{name}', names)
        # print(name)
        if name in names:
            print(name)


names = list_maker()
remove_files_from_dir(sys.argv[2], names)