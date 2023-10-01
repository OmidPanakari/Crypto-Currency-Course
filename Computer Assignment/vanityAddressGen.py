import hashlib
import ecdsa
import base58
import os

def generate_address():
    # Generate a random private key
    random_string = os.urandom(400)
    private_key = hashlib.sha256(hashlib.sha256(random_string).digest()).digest()

    # Create ECDSA public key 
    private_key_hex = private_key.hex()
    private_key_ecdsa = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1) 
    public_key = private_key_ecdsa.get_verifying_key()
    public_key_bytes = b'\x04' + public_key.to_string() 

    # Hash public key
    public_key_hash = hashlib.sha256(public_key_bytes).digest()
    hash_object = hashlib.new('ripemd160')
    hash_object.update(public_key_hash)
    public_key_hash = hash_object.digest()

    # Add testnet prefix 0x6f to public key hash
    public_key_hash = b'\x6f' + public_key_hash  

    checksum = hashlib.sha256(hashlib.sha256(public_key_hash).digest()).digest()[:4]

    # Encode as base58 address 
    address = base58.b58encode(public_key_hash + checksum) 

    # No compression 
    wif = b'\xef' + private_key
    checksum = hashlib.sha256(hashlib.sha256(wif).digest()).digest()[:4]
    wif = base58.b58encode(wif + checksum)  

    return wif.decode('ascii'), public_key_bytes.hex(), address.decode('ascii')

target = 'low'
while True:
    wif, public_key, address = generate_address()
    if address[1:4] == target:
        print("Private key (WIF):", wif)
        print("Public key:", public_key)  
        print("Address:", address)
        break