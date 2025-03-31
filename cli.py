import argparse #what does this do
from key_utils import generate_keypair, save_key, load_key
from crypto_utils import encrypt_file, decrypt_file

def main():
    parser = argparse.ArgumentParser(description="Post-Quantum File Encryption Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Key generation
    keygen_parser = subparsers.add_parser("keygen", help="Generate Kyber key pair")
    keygen_parser.add_argument("--prefix", default="kyber", help="Key filename prefix")

    # Encryption
    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a file")
    encrypt_parser.add_argument("file", help="File to encrypt")
    encrypt_parser.add_argument("--public-key", required=True, help="Recipient's public key")
    encrypt_parser.add_argument("--output", help="Output file path")

    # Decryption
    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt a file")
    decrypt_parser.add_argument("file", help="File to decrypt")
    decrypt_parser.add_argument("--private-key", required=True, help="Your private key")
    decrypt_parser.add_argument("--output", help="Output file path")

    args = parser.parse_args()

    if args.command == "keygen":
        pub, priv = generate_keypair()
        save_key(pub, f"{args.prefix}_public.key")
        save_key(priv, f"{args.prefix}_private.key")
        print(f"Keys generated: {args.prefix}_public.key, {args.prefix}_private.key")

    elif args.command == "encrypt":
        public_key = load_key(args.public_key)
        encrypted_data = encrypt_file(args.file, public_key)
        output_path = args.output or f"{args.file}.enc"
        with open(output_path, 'wb') as f:
            f.write(encrypted_data)
        print(f"File encrypted: {output_path}")

    elif args.command == "decrypt":
        private_key = load_key(args.private_key)
        decrypted_data = decrypt_file(args.file, private_key)
        output_path = args.output or args.file.replace('.enc', '.dec')
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
        print(f"File decrypted: {output_path}")

if __name__ == "__main__":
    main()