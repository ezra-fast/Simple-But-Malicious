''' This script takes a directory as input and creates a backup thereof with a name the user designates '''
import os
import shutil

def directory_getter():
    print("Enter the full path of the directory that you would like to backup or E to exit: ")
    dir = input("> ")
    if dir == 'E' or dir == 'e':
        exit(0)
    return dir

def backer_upper(dir):
    print("Enter the name of the new backed up directory")
    new_dir = input("> ")
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    files = os.listdir(dir)         # all files are available in the 'files' list by file name only -- not full path

    full_path_list = []

    for file in files:
        path_to_file = dir + '\\' + file        # all files in dir are hereby accessible via path_to_file
        new_file_path = new_dir + '\\' + file
        full_path_list.append(path_to_file)      # storing the full paths to all files just in case they need to be referenced
        if os.path.isdir(path_to_file):
            shutil.copytree(path_to_file, new_file_path)
        elif os.path.isfile(path_to_file):
            shutil.copy2(path_to_file, new_file_path)

def main():
    while(1):
        try:
            dir = directory_getter()
            backer_upper(dir)
        except KeyboardInterrupt:
            exit(0)
        print("\nSuccess.\n")
main()