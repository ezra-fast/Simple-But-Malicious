''' This script recursively checks a base directory for permissions, returning directories that an ordinary process would have write access to.
    The purpose of this script is to find directories that would be susceptible to being scrambled by ransomware.
    This script is for "penetration testing" and "security research", just like every tool used in every breach ever.
'''

''' Steps:
    1. traverse base directory recursively
    2. check if the directory has write permissions
    3. if the directory does not, pass
    4. if it does, add the full path to list of writeable_dirs
    5. output all dirs in writeable_dirs
'''

import os

def traverse_recursively(dir):
    try:
        for file in os.listdir(dir):
            full_path = dir + '\\' + file
            if (os.path.isdir(full_path)):
                if (os.access(full_path, os.W_OK)):
                    print(f'{full_path} IS WRITEABLE')
                else:
                    print(f'{full_path} NOT WRITEABLE')
                traverse_recursively(full_path)
            else:
                # print(full_path)
                pass
    except (PermissionError, KeyboardInterrupt) as error:
        if isinstance(error, PermissionError):
            print('Permission Error')
            pass
        elif isinstance(error, KeyboardInterrupt):
            print('Keyboard Interrupt')
            exit(0)

def main():
    traverse_recursively(r'C:\Users')

main()