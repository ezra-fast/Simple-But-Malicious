''' This script will perform basic AES symmetric encryption/decryption '''

# argument 1 is the file being decrypted, argument 2 is the file with key information.

import os 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
import sys
import re

def program_warning():
    print('This script will decrypt the given input file and create a copy with the plaintext. The original ciphertext will be left intact in case there are problems with decryption.')

def extract_keys_from_file():
    input_file = sys.argv[2]
    with open(input_file, 'rb') as file:
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

nepo = sys.argv[1]
with open(nepo, 'rb') as file:
    cipher_text = file.read()
keys = extract_keys_from_file()
new_file = f'{nepo}_DECRYPTED.txt'
secret_key = keys[0]
initialization_vector = keys[1]
cipher_object = Cipher(algorithms.AES(secret_key), modes.CBC(initialization_vector))
decryptor_object = cipher_object.decryptor()
decrypted_text = decryptor_object.update(cipher_text) + decryptor_object.finalize()                 # Padding needs to be removed after decryption because of the decryption method
with open(new_file, 'w') as file:
    for letter in decrypted_text:
        if chr(letter).isascii() == True:                                                           # Padding ended up not being removed because it was overly arduous :(
            file.write(chr(letter))