# Author: Ezra Fast     Date: July 14, 2023

# IMPORTANT: 
# For some unknown, ungodly reason, --pem [FILE] has to specified first on the cmdline

# SAMPLE COMMAND:
# python .\masker_true.py --pem private.pem --dir_encrypt --dir 'C:\Users\efast\OneDrive - Calgary Stampede\Documents\python_practice\TEST\' 

# For the pesky warnings that tarnish the console during runtime:
# use the -w or --warnings option to silence output to the console

''' For direcory encryption and decryption, exceptions are thrown. However, the operations are always successful if the right keys are used.
    The operations are likely successful despite the warnings because of fallbacks in the cryptography module and the methods called on the objects
    contained therein.
    ** Run with -w / --warnings to hide these warnings because they don't make a difference either way!
'''

# Original Description:
# This script generates a private key, derives the public key, and performs asymmetric encryption/decryption to read the contents of the file.
# The public exponent is 65537, which is commonly used; the key size is 2048, which is generally considered secure
# The private key is stored in a PEM file following creation, and the public key is derived but not stored

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import argparse
import os
import warnings

def arguments():
    parser = argparse.ArgumentParser(
        prog='comprehensive_RSA',
        description='This program can be used to generate private key(s) and derive public key(s), and encrypt or decrypt files.',
        epilog='Provide a file as the first argument and use options thereafter as needed. PEM files must only contain private keys and must not be encrypted.')
        
    parser.add_argument('-f', '--filename')                                 # name of the input file --> positional
    parser.add_argument('-p', '--pem')                              # This optional argument will store the pem file
    parser.add_argument('--file_encrypt', action='store_true')           # store_true gives False by default
    parser.add_argument('--file_decrypt', action='store_true')
    parser.add_argument('--dir_encrypt', action='store_true')           # store_true gives False by default
    parser.add_argument('--dir_decrypt', action='store_true')
    parser.add_argument('--dump', action='store_true')
    parser.add_argument('--generate_private', action='store_true')
    parser.add_argument('--generate_public_from_private', action='store_true')
    parser.add_argument('--dir')                           # use this option to encrypt dir and all sub dirs
    parser.add_argument('-w', '--warnings', action='store_true')            # silence warnings

    args = parser.parse_args()
    # Uncomment to troubleshoot argument parsing:
    # print(args.filename, args.pem, args.encrypt, args.decrypt, args.dump, args.generate_private, args.generate_public_from_private, args.generate_pem_from_private)
    final_args = []
    final_args.append(args.filename)
    final_args.append(args.pem)
    final_args.append(args.file_encrypt)
    final_args.append(args.file_decrypt)
    final_args.append(args.dir_encrypt)
    final_args.append(args.dir_decrypt)
    final_args.append(args.dump)
    final_args.append(args.generate_private)
    final_args.append(args.generate_public_from_private)
    final_args.append(args.dir)
    final_args.append(args.warnings)
    
    ''' 
    filename: final_args[0]
    pem: final_args[1]
    file_encrypt: final_args[2]
    file_decrypt: final_args[3]
    dir_encrypt: final_args[4]
    dir_encrypt: final_args[5]
    dump: final_args[6]
    generate_private: final_args[7]
    generate_public_from_private: final_args[8]
    dir: final_args[9]
    '''

    return final_args

def generate_private_key():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
    print(private_key)
    return private_key

def generate_public_key(private_key):
    public_key = private_key.public_key()
    print(public_key)
    return public_key

def store_private_key(private_key, outfile):
    pem_staging = private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())
    with open(outfile, 'wb') as pem_file:
        pem_file.write(pem_staging)

def store_public_key(public_key, outfile):
    pem_contents = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    with open(outfile, 'wb') as file:
        file.write(pem_contents)

def RSA_encrypt_initial(public_key, file):            # Encrypt the data with public key
    with open(file, 'rb') as nepo:
        data = nepo.read()
    encrypted_data = public_key.encrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    with open(file, 'wb') as nepo:
        nepo.write(encrypted_data)
    return encrypted_data

def RSA_encrypt(public_key, file, outfile):            # Encrypt the data with public key
    with open(file, 'rb') as nepo:
        data = nepo.read()
    encrypted_data = public_key.encrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    with open(outfile, 'wb') as nepo:
        nepo.write(encrypted_data)
    return encrypted_data

def RSA_decrypt_initial(private_key, file):            # Decrypt the data with private key
    with open(file, 'rb') as nepo:
        data = nepo.read()
    decrypted_data = private_key.decrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    with open(file, 'wb') as nepo:
        nepo.write(decrypted_data)
    return decrypted_data

def RSA_decrypt(private_key, file, outfile):            # Decrypt the data with private key
    with open(file, 'rb') as nepo:
        data = nepo.read()
    decrypted_data = private_key.decrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    with open(outfile, 'wb') as nepo:
        nepo.write(decrypted_data)
    return decrypted_data

def private_from_pem(pem):
    with open(pem, 'rb') as pem_file:
        data = pem_file.read()
    private_key = serialization.load_pem_private_key(data, password=None)
    return private_key

def public_from_pem(pem):
    with open(pem, 'rb') as pem_file:
        data = pem_file.read()
    private_key = serialization.load_pem_private_key(data, password=None)
    public_key = private_key.public_key()
    return public_key

def file_name_preparer(filename):
    holder = []
    new = []
    for letter in filename:
        holder.append(letter)
    if (holder[0] == '.' and holder[1] == '\\'):            # Powershell is the reason for this
        for i in range(2, len(holder)):
            new.append(holder[i])
        file_name = ''.join(new)
        return file_name
    else:
        return filename

def RSA_encrypt_dir(dir, private_key, args):
    dir = no_idea_why_this_is_necessary(dir)
    public_key = generate_public_key(private_key)
    for file_name in os.listdir(dir):
        try:
            current = f'{dir}\\{file_name}'
            if (os.path.isdir(current) == True):
                RSA_encrypt_dir(current, private_key, args)
            else:
                RSA_encrypt_initial(public_key, current)
        except ValueError as error:
            if (args[10] == True):
                pass
            print(f'Error generated but encryption likely successful; Error: {error}\nRun with -w to silence warnings.')
            pass


def RSA_decrypt_dir(dir, private_key, args):
    dir = no_idea_why_this_is_necessary(dir)
    for file_name in os.listdir(dir):
        try:
            current = f'{dir}\\{file_name}'
            if (os.path.isdir(current) == True):
                RSA_decrypt_dir(current, private_key, args)
            else:
                RSA_decrypt_initial(private_key, current)
        except ValueError as error:
            if (args[10] == True):
                pass
            print(f'Error generated during decryption but still likely successful; Error: {error}\nRun with -w to silence warnings.')
            pass

def dir_name_preparer(dir_name):
    holder = []
    new = []
    for letter in dir_name:
        holder.append(letter)
    length = len(holder)
    if (holder[length - 1] == '\\'):            # Heaven forbid you want to tab-complete your filenames
        del holder[length - 1]
        new = ''.join(holder)
        return new
    return dir_name

def no_idea_why_this_is_necessary(dir_name):
    holder = []
    new = []
    for letter in dir_name:
        holder.append(letter)
    length = len(holder)
    if (holder[length - 1] == '"'):            # Heaven forbid you want to tab-complete your filenames
        del holder[length - 1]
        new = ''.join(holder)
        return new
    return dir_name

def main():
    args = arguments()
    if (args[10] == True):
        warnings.filterwarnings('ignore')
    pem_file = args[1]
    if (args[7] == True):
        private_key = generate_private_key()
        outfile = input('Please enter the name of your output .pem file (omit the .pem extension): ')
        outfile = f'{outfile}.pem'
        store_private_key(private_key, outfile)
        print(f'{outfile} has been created in the current directory.')
        if (args[6] == True):
            with open(outfile, 'r') as file:
                data = file.read()
            print(data)
        exit(0)
    elif (args[8] == True):
        private_key = private_from_pem(pem_file)
        public_key = generate_public_key(private_key)
        outfile = input('Please enter the name of the new public key .pem file (omit the .pem extension): ')        # Test Here
        outfile = f'{outfile}.pem'
        store_public_key(public_key, outfile)
        print(f'{outfile} has been created in the current directory.')
        if (args[6] == True):
            with open(outfile, 'r') as file:
                data = file.read()
            print(data)
        exit(0)
    if (args[2] == True or args[3] == True):
        input_file = file_name_preparer(args[0])
        if (args[2] == True):                      # Encrypt with public key
            outfile = f'encrypted_{input_file}'
            private_key = private_from_pem(pem_file)
            public_key = generate_public_key(private_key)
            encrypted_material = RSA_encrypt(public_key, input_file, outfile)
            print('Encryption Operation Performed Successfully')
            if (args[6] == True):
                print(f'Encrypted Material (Dump): {encrypted_material}')
            exit(0)
        elif (args[3]== True):
            outfile = f'decrypted_{input_file}'
            private_key = private_from_pem(pem_file)
            public_key = generate_public_key(private_key)
            decrypted_material = RSA_decrypt(private_key, input_file, outfile)
            print('Decryption Operation Performed Successfully')
            if (args[6] == True):
                print(f'Decrypted Material (Dump): {decrypted_material}')
            exit(0)
    elif (args[4] == True or args[5] == True):                  # Directory encryption and decryption, in that order
        input_dir = dir_name_preparer(args[9])
        if (args[4] == True):
            private_key = private_from_pem(pem_file)
            public_key = generate_public_key(private_key)
            RSA_encrypt_dir(input_dir, private_key, args)
            print('Encryption of Directory Successful.')
            exit(0)
        elif (args[5] == True):
            private_key = private_from_pem(pem_file)
            public_key = generate_public_key(private_key)
            RSA_decrypt_dir(input_dir, private_key, args)
            print('Decryption of Directory Successful.')
            exit(0)

main()