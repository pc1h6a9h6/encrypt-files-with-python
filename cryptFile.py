#!/usr/bin/python3

import os
import sys
from Crypto import Random
from Crypto.Cipher import AES

opt = 99
ext = ""

def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key, key_size=256):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

def encrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    enc = encrypt(plaintext, key)
    with open(file_name + ".pc1", 'wb') as fo:
        fo.write(enc)

def decrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        ciphertext = fo.read()
    dec = decrypt(ciphertext, key)
    with open(file_name[:-4], 'wb') as fo:
        fo.write(dec)


def encrypt_all_files(dirName):
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]

    for file in listOfFiles:
        print('Encrypting ', file)
        try:
            encrypt_file(file, key)
            if opt == 3:
                os.remove(file)
        except:
            print('  ERROR encrypting ', file)

def decrypt_all_files(dirName):
    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(dirName):
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]

    for file in listOfFiles:
        print('Decrypting ', file)
        try:
            decrypt_file(file, key)
            if opt == 4:
                os.remove(file)
        except:
            print('  ERROR decrypting ', file)


#show options
print(' 1-Encrypt (do not delete the original files)')
print(' 2-Decrypt (do not delete the original files)')
print(' 3-Encrypt   (delete the original files)')
print(' 4-Decrypt   (delete the original files)')
print(' 99-Exit\n')

# insert option
opt = int(input('pc1> '))

# encode the key
key = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'
print('key=',key)
# Exit option
if opt == 99:
    sys.exit(0)

dirname = str(input('Directory path: '))

if opt == 1 or opt == 3:
    encrypt_all_files(dirname)
elif opt == 2 or opt == 4:
    decrypt_all_files(dirname)
else:
    print('Invalid option !!!')
