import hashlib
import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from openpgp import openpgp_encrypt, openpgp_decrypt

'''
cryptography depends on the OpenSSL C library for all cryptographic operation.
OpenSSL is the de facto standard for cryptographic libraries and provides high
performance along with various certifications that may be relevant to developers.
'''

passphrase = b"passphrase"

##load
if os.path.exists("private_key.pem"):
  with open("private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
      key_file.read(),
      password=passphrase,
    )
  print("Key loaded successfully!")
else:
  private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

public_key = private_key.public_key()

##save
with open("private_key.pem", "wb") as f:
    '''
    Every time you run private_key.private_bytes(...),
    a new random "salt" is generated,
    making the final encrypted text look completely new.

    Since you cannot trust the file's visual appearance,
    you need to look at the Key Fingerprint.
    A fingerprint is a "hash" (a short, unique string) of the key.
    If two keys have the same fingerprint, they are identical.
    '''
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(passphrase),
    ))

# 1. Get the public key bytes in a standard format
public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.DER, # Use DER for a stable "identity"
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)
# 2. Create a SHA-256 hash (the fingerprint)
fingerprint = hashlib.sha256(public_bytes).hexdigest()
print(f"Key Fingerprint: {fingerprint}")

with open("public_key.pem", "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

if __name__ == "__main__":
  # openpgp_encrypt(public_key=public_key)
  openpgp_decrypt(private_key=private_key)