# pqcrypt-cli

A CLI tool that:

- **Encrypts a file**:
  - Uses **Kyber** to securely share an **AES-256** key.
  - Encrypts the actual file with **AES-256-GCM** (fast and secure).
  
- **Decrypts the file**:
  - Uses **Kyber** to recover the AES key.
  - Decrypts the file with **AES**.

## The Key Exchange
- **Kyber** replaces **RSA/ECDH** for securely exchanging keys.

## File Encryption
- **AES-256-GCM** is a symmetric encryption algorithm, meaning we use the same key to both encrypt and decrypt the file.

## Why Not Encrypt the Whole Thing with Kyber?

1. **Kyber** is mainly used for **Key Encapsulation Mechanism (KEM)** to securely exchange keys between two parties.
   - **Kyber** is slow for large data.
   - It is designed for **key exchange** (encrypting small keys), not for bulk encryption.
   
   Example: 
   - **Kyber** encrypts ~10KB/sec.
   - **AES** encrypts ~1GB/sec.

2. **Kyber ciphertexts** are around **1KB** per encrypted message.
   - Encrypting a file chunk-by-chunk would inflate the file size massively (e.g., a 1MB file becomes ~100MB).

3. **Symmetric encryption** is also quantum-resistant.
   - **AES-256** (or **ChaCha20**) is already secure against quantum attacks when using a 256-bit key.
   - The real quantum threat is to **asymmetric cryptography** (like **RSA/ECC/Kyber**). But why is this the case?

## Why Combine Kyber + AES? 
This is called **hybrid encryption** (used in protocols like TLS, PGP, etc.).

1. **Kyber's Role**:
   - Securely exchange an AES key.
   - Encrypt the AES key.

2. **AES's Role**:
   - Encrypt the actual file at high speed.

3. **Final Output**:
   - [Kyber-encrypted AES key] + [AES-encrypted file]

## Step-by-Step File Transfer (You → Friend X)

### Key Setup
- Friend X generates a **Kyber key pair** (`x_private_key`, `x_public_key`) and sends you the `x_public_key` (Public keys are safe to share!).

### You Encrypt the File
1. Generate a random **AES-256 key** (single-use):
```python
   aes_key = os.urandom(32)  # 256-bit key
```

### Encrypt the file with AES-GCM:

```python
cipher = AES.new(aes_key, AES.MODE_GCM)
encrypted_file, tag = cipher.encrypt_and_digest(file_data)
nonce = cipher.nonce  # Unique per encryption
```

### Encrypt the AES key with X’s public key (using Kyber):

```python
encrypted_aes_key = kyber.encrypt(x_public_key, aes_key)
```

### Send the Package

Combine everything into one file and send:
[encrypted_aes_key] + [nonce] + [tag] + [encrypted_file]
(Example: encrypted_data.pqc)
Friend X Decrypts the File
Split the received file into its parts.
Decrypt the AES key with X’s private key (using Kyber):

```python
aes_key = kyber.decrypt(x_private_key, encrypted_aes_key)
```

Decrypt the file with AES-GCM:

```python
cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
file_data = cipher.decrypt_and_verify(encrypted_file, tag)
```

## 🔑 Key Clarifications

### Why AES?

Kyber is only for encrypting the small AES key (fast key exchange).

AES is used to encrypt the actual file (bulk data).

### Why Nonce and Tag?

Nonce: Ensures uniqueness (never reuse with the same key!).

Tag: Ensures the file hasn’t been tampered with (authentication).

### Security Guarantees

Only X can decrypt: The AES key is locked with X’s public key.

Quantum-resistant: Kyber protects the AES key from future quantum attacks.

📜 Example File Format
Offset	Content
0-767	- Kyber-encrypted AES key (768 bytes for Kyber512)
768-779 - 	AES nonce (12 bytes)
780-795 - 	AES tag (16 bytes)
796-end -	AES-encrypted file