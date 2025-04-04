#key generation/managment
from secrets import compare_digest
from pqcrypto.kem.kyber512 import generate_keypair, encrypt, decrypt
import os

def Generate_keypair():
    #Generate Kyber public/private keys.
    public_key, private_key = generate_keypair()
    return public_key, private_key 

# a,b = Generate_keypair()
# print(a, b)

def save_key(key, filename):
    #saves key to the file
    with open(filename,"wb") as f:
        f.write(key)
def load_key(filename):
    with open(filename, "rb") as f:
        return f.read()
    