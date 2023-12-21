# This script generates a private key, derives the public key, and performs asymmetric encryption/decryption to read the contents of the file.

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

def generate_private_key():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    print(private_key)
    return private_key

def generate_public_key(private_key):
    public_key = private_key.public_key()
    print(public_key)
    return public_key

def store_private_key(private_key):
    pem_staging = private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())
    with open('private_key_pem.pem', 'wb') as pem_file:
        pem_file.write(pem_staging)

def RSA_encrypt(public_key, file):            # Encrypt the data with public key
    with open(file, 'rb') as nepo:
        data = nepo.read()
    encrypted_data = public_key.encrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    with open(file, 'wb') as nepo:
        nepo.write(encrypted_data)
    return encrypted_data

def RSA_decrypt(private_key, file):
    with open(file, 'rb') as nepo:
        data = nepo.read()
    decrypted_data = private_key.decrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    with open(file, 'wb') as nepo:
        nepo.write(decrypted_data)
    return decrypted_data

''' Steps:
    1. Take file in 
    2. generate public and private keys
    3. store private keys
    4. encrypt the file
    5. decrypt the file'''


def main():
    file = 'z.txt'
    private_key = generate_private_key()
    public_key = generate_public_key(private_key)
    store_private_key(private_key)
    print(RSA_encrypt(public_key, file))
    RSA_decrypt(private_key, file)
    # print(RSA_decrypt(private_key, file))

main()