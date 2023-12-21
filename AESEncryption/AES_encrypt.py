''' This script will perform basic AES symmetric encryption/decryption '''

# Padding is done manually because the cryptography library tends to make padding overly complicated relative to my purposes.

# argument 1 is the name of the file that is being encrypted.

# To save the unencrypted padding and the length of the padding comment the lines back in.

import os 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
import sys

def program_warning():
    print('This script will encrypt input files using the AES-256 encryption algorithm.\nUpon encryption of material, this program will output both the symmetric 256-bit encryption key and the 128-bit initialization vector to an output file called key_material.txt.\nThe number of padded bytes will be output to a file called padding.txt.\nThe destined decryptor of the cipher material requires the information in these files for decryption.\nKnowing that this program can irreversibly alter files, enter y to continue.')
    answer = input('>> ')
    if answer == 'y' or answer == 'Y':
        return 0
    else:
        exit(0)

def pad_length_calculator(data, block_size):
    padding_length = block_size - (len(data) % block_size)
    return padding_length

def pad_data(data, block_size):
    padding_length = block_size - (len(data) % block_size)
    # padding = bytes([padding_length] * padding_length)            # this pads with the same byte over and over again
    padding = os.urandom(padding_length)
    with open('padding_info.txt', 'wb') as file:
        file.write(padding)
    return data + padding

def save_key_to_pem(key_bytes, iv_bytes):
    filename = 'key_material.pem'
    iv_base64 = base64.b64encode(iv_bytes) 
    key_base64 = base64.b64encode(key_bytes)
    note1 = b'Initialization Vector: '
    note2 = b' Symmetric Key: '
    with open(filename, 'wb') as file:
        file.write(note1)
        file.write(iv_base64)
        file.write(note2)
        file.write(key_base64)

# def save_pad_length(length):
#     with open('padding.txt', 'w') as file:
#         file.write(str(length))

nepo = sys.argv[1]
with open(nepo, 'rb') as file:
    plain_text = file.read()
plain_text = pad_data(plain_text, 16)
pad_length = pad_length_calculator(plain_text, 16)
secret_key = os.urandom(32)                                         # 32 byte/256 bit symmetric key
initialization_vector = os.urandom(16)
save_key_to_pem(secret_key, initialization_vector)
# save_pad_length(pad_length)
cipher_object = Cipher(algorithms.AES(secret_key), modes.CBC(initialization_vector))
encryptor_object = cipher_object.encryptor()
cipher_text = encryptor_object.update(plain_text) + encryptor_object.finalize()
decryptor_object = cipher_object.decryptor()
decrypted_text = decryptor_object.update(cipher_text) + decryptor_object.finalize()
with open(nepo, 'wb') as file:
    file.write(cipher_text)