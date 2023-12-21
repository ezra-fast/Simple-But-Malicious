from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os


def encrypt_file(file_path, public_key_path):
    # Load the public key from file
    with open(public_key_path, 'rb') as f:
        public_key = RSA.import_key(f.read())

    # Generate a cipher using the public key
    cipher_rsa = PKCS1_OAEP.new(public_key)

    # Read the content of the file
    with open(file_path, 'rb') as f:
        file_content = f.read()

    # Encrypt the file content
    encrypted_content = cipher_rsa.encrypt(file_content)

    # Create a new file with the encrypted content
    encrypted_file_path = file_path + ".encrypted"
    with open(encrypted_file_path, 'wb') as f:
        f.write(encrypted_content)

    print("File encrypted:", encrypted_file_path)


def main():
    # Specify the file path and public key path
    file_path = "path/to/your/file"
    public_key_path = "path/to/your/public/key.pem"

    # Encrypt the file
    encrypt_file(file_path, public_key_path)


if __name__ == "__main__":
    main()
