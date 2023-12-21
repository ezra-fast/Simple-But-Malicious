''' This script works to count the number of files in a specified directory '''
import os
def count_files(directory):
    counter_files = 0
    file_list = os.listdir(directory)
    for file in file_list:
        if os.path.isfile(file):
            counter_files = counter_files + 1
    return counter_files
def directory_getter():
    print("Enter a directory path in the following format: C:\\Users\\efast\\Documents")
    dir_path = input("> ")
    return dir_path
def main():
    dir_path = directory_getter()
    num_files = count_files(dir_path)
    if num_files < 1:
        print("Invalid Director Entry or Permission Denied")
        exit()
    print(f"There are {num_files} files in that directory")
main()