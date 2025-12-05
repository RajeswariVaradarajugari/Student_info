from ecies.keys import PrivateKey
from ecies import encrypt, decrypt

private_key = PrivateKey('secp256k1')
public_key = private_key.public_key 
print(f"Private key: {private_key.to_hex()}")
print(f"Public key: {public_key.to_hex()}")
data = b"Hello, this is a test message."
encrypted_msg = encrypt(private_key.to_bytes(), data)

print(f"Encrypted message: {encrypted_msg.hex()}")  
decrypted_msg = decrypt(private_key, encrypted_msg)
print(f"Decrypted message: {decrypted_msg.decode('utf-8')}")