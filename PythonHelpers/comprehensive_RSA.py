# Author: Ezra Fast     Date: July 14, 2023

# Original Description:
# This script generates a private key, derives the public key, and performs asymmetric encryption/decryption to read the contents of the file.
# The public exponent is 65537, which is commonly used; the key size is 4096 (originally 2048), which is generally considered secure
# The private key is stored in a PEM file following creation, and the public key is derived but not stored

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import argparse

def arguments():
    parser = argparse.ArgumentParser(
        prog='comprehensive_RSA',
        description='This program can be used to generate private key(s) and derive public key(s), and encrypt or decrypt files.',
        epilog='Provide a file as the first argument and use options thereafter as needed. PEM files must only contain private keys and must not be encrypted.')
        
    parser.add_argument('-f', '--filename')                                 # name of the input file --> positional
    parser.add_argument('-p', '--pem')                              # This optional argument will store the pem file
    parser.add_argument('--encrypt', action='store_true')           # store_true gives False by default
    parser.add_argument('--decrypt', action='store_true')
    parser.add_argument('--dump', action='store_true')
    parser.add_argument('--generate_private', action='store_true')
    parser.add_argument('--generate_public_from_private', action='store_true')

    args = parser.parse_args()
    # Uncomment to troubleshoot argument parsing:
    # print(args.filename, args.pem, args.encrypt, args.decrypt, args.dump, args.generate_private, args.generate_public_from_private, args.generate_pem_from_private)
    final_args = []
    final_args.append(args.filename)
    final_args.append(args.pem)
    final_args.append(args.encrypt)
    final_args.append(args.decrypt)
    final_args.append(args.dump)
    final_args.append(args.generate_private)
    final_args.append(args.generate_public_from_private)
    
    return args

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

''' Still needs:
    1. --encrypt or --decrypt option
    2. --generate private 
    3. --generate public-from-private
    4. --generate public-from-pem
    5. --dump --> true or false option to dump decrypted contents to console after decryption'''

def main():
    args = arguments()
    pem_file = args.pem
    if (args.generate_private == True):
        private_key = generate_private_key()
        outfile = input('Please enter the name of your output .pem file (omit the .pem extension): ')
        outfile = f'{outfile}.pem'
        store_private_key(private_key, outfile)
        print(f'{outfile} has been created in the current directory.')
        if (args.dump == True):
            with open(outfile, 'r') as file:
                data = file.read()
            print(data)
        exit(0)
    elif (args.generate_public_from_private == True):
        private_key = private_from_pem(pem_file)
        public_key = generate_public_key(private_key)
        outfile = input('Please enter the name of the new public key .pem file (omit the .pem extension): ')        # Test Here
        outfile = f'{outfile}.pem'
        store_public_key(public_key, outfile)
        print(f'{outfile} has been created in the current directory.')
        if (args.dump == True):
            with open(outfile, 'r') as file:
                data = file.read()
            print(data)
        exit(0)
    if (not args.filename):
        print('No input file given')
        exit(0)
    else:
        input_file = file_name_preparer(args.filename)
    if (args.encrypt == True):                      # Encrypt with public key
        outfile = f'encrypted_{input_file}'
        private_key = private_from_pem(pem_file)
        public_key = generate_public_key(private_key)
        encrypted_material = RSA_encrypt(public_key, input_file, outfile)
        print('Operation Performed Successfully')
        if (args.dump == True):
            print(f'Encrypted Material (Dump): {encrypted_material}')
        exit(0)
    elif (args.decrypt == True):
        outfile = f'decrypted_{input_file}'
        private_key = private_from_pem(pem_file)
        public_key = generate_public_key(private_key)
        decrypted_material = RSA_decrypt(private_key, input_file, outfile)
        print('Operation Performed Successfully')
        if (args.dump == True):
            print(f'Decrypted Material (Dump): {decrypted_material}')
        exit(0)
    
main()


'''string = 'z.txt\\'
filename = file_name_preparer(string)
print(filename)'''


'''preliminary main function:
def main():
    # file = 'z.txt'
    # private_key = generate_private_key()
    # public_key = generate_public_key(private_key)
    # store_private_key(private_key)
    # print(RSA_encrypt(public_key, file))
    # RSA_decrypt(private_key, file)
'''