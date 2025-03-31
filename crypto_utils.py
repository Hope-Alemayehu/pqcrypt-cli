#Encryption and decryption logic
from pqcrypto.kem.kyber512 import encrypt as kyber_encrypt, decrypt as kyber_decrypt 
from Crypto.Cipher import AES 
from Crypto.Util.Padding import pad, unpad  # what does these two do
import os 

def encrypt_file(file_path, public_key):
    #encrypts the file using hybrid  Kyber + AES approches 
    
    #generate a rondom key
    aes_key = os.random(32)
    
    #we encrypt the AES key using the public key
    encrypted_aes_key = kyber_encrypt(public_key, aes_key)
    
    #encrypt the file with AES 
    iv = os.urandom(16) #nounce
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    with open(file_path, "rb") as f:
        plaintext = f.read()
        
    ciphertext = cipher.encrypt(pad(plaintext,AES.block_size))
    return encrypted_aes_key + iv + ciphertext 

def decrypt_file(encrypted_path, private_key):
    #decrypt file using the hybrid kyber+AES approch
    with open(encrypt_file, 'rb') as f:
        data = f.read()
    
    # we split the components
    encrypted_aes_key = data[:1088]  #kyber512 ciphertext size 
    iv = data[1088: 1104]
    ciphertext = data[1104:]
    
    #Decrypt AES key with kyber
    aes_key = kyber_decrypt(private_key, encrypted_aes_key)
    
    #decrypt file with AES
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    
    return plaintext
    