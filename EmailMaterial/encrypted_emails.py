# Author: Ezra Fast     Date: July 17, 2023

'''
This script will take in the necessary inputs to send the body of an email to the recipient as an encrypted file.
'''

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import argparse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import getpass          # getpass.getpass never worked in the test environment, uncomment to use
import sys

def arguments():
    parser = argparse.ArgumentParser(
        prog='outlook_RSA_emailer',
        description='This program can be used to encrypt the body of an outlook email and send it to the specified recipient.',
        epilog='Provide a source outlook email address, private key pem file, and .txt file (body of email) as cmdline input.')

    parser.add_argument('-s', '--source_address')
    parser.add_argument('-b', '--body')        
    parser.add_argument('-p', '--pem')                              # This optional argument will store the pem file
    parser.add_argument('--decrypt', action='store_true')
    parser.add_argument('-f', '--file')

    args = parser.parse_args()
    
    return args

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
    return outfile

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

def emailer(args):
    source_address = args.source_address
    body = args.body
    pem_file = args.pem
    server = 'smtp-mail.outlook.com'
    port = 587
    connection = smtplib.SMTP(server, port)
    connection.starttls()
    password = 'NOTHINGTOSEEHERE' # getpass.getpass("Enter your email password: ") # input('Enter your email password:\n>>') 
    connection.login(source_address, password)
    subject_line = input('Enter the subject line:\n>>')
    recipient = input("Enter the recipient address:\n>>")
    message_container = MIMEMultipart()
    message_container['From'] = source_address
    message_container['To'] = recipient
    message_container['Subject'] = subject_line

    private_key = private_from_pem(pem_file)
    public_key = generate_public_key(private_key)
    outfile = input("Call the encrypted attachment:\n>>")
    print(outfile)
    outbound_file = RSA_encrypt(public_key, body, outfile)
    
    with open(outbound_file, 'rb') as file:
        data = MIMEApplication(file.read(), Name=outbound_file)
        data['Content-Disposition'] = f'attachment; filename="{outbound_file}"'
        message_container.attach(data)
    connection.send_message(message_container)
    print("Encrypted Email Sent")
    # except Exception as exception:
    # print(f'Exception Raised; The Problem: {exception}')
    connection.quit()

def email_decrypt(args):
    infile = args.file
    pem = args.pem
    private_key = private_from_pem(pem)
    public_key = generate_public_key(private_key)
    RSA_decrypt_initial(private_key, infile)
    print("Decryption Successful.")
    exit(0)

def main():
    args = arguments()
    if (args.decrypt == True):
        email_decrypt(args)
    else:
        emailer(args)

main()
