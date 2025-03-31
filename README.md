# pqcrypt-cli
a CLI tool that:  
- Encrypts a file:
  - Uses Kyber to securely share an AES-256 key.
  - Encrypts the actual file with AES-256-GCM (fast and secure).
- Decrypts the file:  Uses Kyber to recover the AES key.  Decrypts the file with AES.


## The Key Exchange
- Kyber replaces RSA/ECDH for securely exhanging keys

## File Encryption
- AES-256-GCM(Symmetric which means we are only using one key to encypt and decrypt) the actual file

## Why not encrypt the whole thing with kyber
1. mainly used for Key Encapsulation mechanishm (KEM) to securly exchange keys between two parties
- Kyber is slow for large data
- In general it is designed for key exchange(encrypting small keys), not bulk encryption

Example: Kyber encrypts ~ 10KB.sec, AES encrypts ~1GB/sec
2. Kyber ciphertexts are ~1KB per encrypted message.
- Encrypting a file chunk-by-chunk would inflate the size massively (e.g., a 1MB file becomes ~100MB).

3. Symmetric encryption is quantum  resistant too 
- AES-256 (chacha20) is an already secure aganist quantum attacks when using 256 bit key 
- the real quantum threat is to asymmetric cryptography(like RSA/ECC/Kyber) ..........why is thisss tho

## Why combine Kyber + AES? 
this is called a hybrid encryption(used in TLS, PGB,...)

1.  KYber role:
- securly exchange an AES key
- encrytp AES key

2. AES role
- encrypt the actual file at high speed

3. final output 

[kyber-encrypted AES key] + [AES-encrypted file]


Step-by-Step File Transfer (You → Friend X)
Key Setup

Friend X generates a Kyber key pair (x_private_key, x_public_key) and sends you x_public_key. (Public keys are safe to share!)

You Encrypt the File

Generate a random AES-256 key (single-use):

python
Copy
aes_key = os.urandom(32)  # 256-bit key
Encrypt the file with AES-GCM:

python
Copy
cipher = AES.new(aes_key, AES.MODE_GCM)
encrypted_file, tag = cipher.encrypt_and_digest(file_data)
nonce = cipher.nonce  # Unique per encryption
Encrypt the AES key with X’s public key (using Kyber):

python
Copy
encrypted_aes_key = kyber.encrypt(x_public_key, aes_key)
Send the Package
Combine into one file and send:

Copy
[encrypted_aes_key] + [nonce] + [tag] + [encrypted_file]
(Example: encrypted_data.pqc)

Friend X Decrypts the File

Split the received file into its parts.

Decrypt the AES key with X’s private key (Kyber):

python
Copy
aes_key = kyber.decrypt(x_private_key, encrypted_aes_key)
Decrypt the file with AES-GCM:

python
Copy
cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
file_data = cipher.decrypt_and_verify(encrypted_file, tag)
🔑 Key Clarifications
Why AES?

Kyber is only for encrypting the small AES key (fast key exchange).

AES encrypts the actual file (bulk data).

Why nonce and tag?

nonce: Ensures uniqueness (never reuse with the same key!).

tag: Ensures the file wasn’t tampered with (authentication).

Security Guarantees

Only X can decrypt: The AES key is locked with X’s public key.

Quantum-resistant: Kyber protects the AES key from future quantum attacks.

📜 Example File Format
Copy
Offset   | Content
─────────────────────────────
0-767    | Kyber-encrypted AES key (768 bytes for Kyber512)  
768-779  | AES nonce (12 bytes)  
780-795  | AES tag (16 bytes)  
796-end  | AES-encrypted file  

