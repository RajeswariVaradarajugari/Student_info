import ecdsa, json

# Generate a new private key using the SECP256k1 curve
private_key = ecdsa.SigningKey.from_string(bytes.fromhex("81e54fb13a011093019fc1b369dc178bf2debfdf06de6071a7656cb8ddab8465"), curve=ecdsa.SECP256k1)

# Derive the public key from the private key
public_key = ecdsa.VerifyingKey.from_string(bytes.fromhex("914e7e8ae2e2b6cbf3d6e3deb3ac1e3e3f33a421df5e9ce75d13085e23ebcffe69ea20381f9fade12e2b1cb0cdf8760572c2237f00f514508d29f7d57697c366"), curve=ecdsa.SECP256k1)

# Output the keys in hexadecimal format
print(f"Private key: {private_key.to_string().hex()}")
print(f"Public key: {public_key.to_string().hex()}")

message = {"Name": "John Doe", "course": "Ms in CS", "joining_year": 2022, "graduated_year": 2024}
byte_wise_json = json.dumps(message).encode('utf-8')
# signature = ecdsa.SigningKey.sign(message, private_key, curve=curve)
# generate
print(byte_wise_json)
signature = private_key.sign_deterministic(byte_wise_json)
print("signature " + signature.hex())
print(public_key.verify(signature, byte_wise_json))