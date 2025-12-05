import ecdsa

# Generate a new private key using the SECP256k1 curve
private_key = ecdsa.SigningKey.from_string(bytes.fromhex("81e54fb13a011093019fc1b369dc178bf2debfdf06de6071a7656cb8ddab8465"), curve=ecdsa.SECP256k1)

# Derive the public key from the private key
public_key = ecdsa.VerifyingKey.from_string(bytes.fromhex("914e7e8ae2e2b6cbf3d6e3deb3ac1e3e3f33a421df5e9ce75d13085e23ebcffe69ea20381f9fade12e2b1cb0cdf8760572c2237f00f514508d29f7d57697c366"), curve=ecdsa.SECP256k1)

# Output the keys in hexadecimal format
print(f"Private key: {private_key.to_string().hex()}")
print(f"Public key: {public_key.to_string().hex()}")

message = b"Hello, this is a test message."

# signature = ecdsa.SigningKey.sign(message, private_key, curve=curve)
# generate
signature = private_key.sign_deterministic(message)
public_key.verify(signdecode=signature, data=message)

print(public_key.verify(signature, message))

print(signature)
print(f"Signature: {signature.hex()}")
new_signature  = private_key.sign_deterministic(message)
print("new signature :", new_signature.hex())
if(new_signature==signature):
    print("signatures are equal")


print(public_key.verify(signature, message))

