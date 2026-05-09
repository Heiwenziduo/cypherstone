import hashlib
import os
from pathlib import Path
import sys
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# from gui.console_screen import cys_console
from script.data import file_path_picker, user_db

'''
cryptography depends on the OpenSSL C library for all cryptographic operation.
OpenSSL is the de facto standard for cryptographic libraries and provides high
performance along with various certifications that may be relevant to developers.
'''

_default_passphrase = b"alohomora"

##
def create_key_pairs(alias: str, key_size=2048, passphrase=_default_passphrase):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )
    public_key = private_key.public_key()

    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(passphrase),
    )
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.DER, # Use DER for a stable "identity"
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    user_db.save_key(
        alias=alias,
        fingerprint=hashlib.sha256(public_bytes).hexdigest(),
        priv_bytes=private_bytes,
        pub_bytes=public_bytes
    )

def import_public_key(alias: str, file_path, password=_default_passphrase):
    # TODO: import private
    '''only public now'''
    with open(file_path, "rb") as key_file:
        # private_key = serialization.load_pem_private_key(
        #   key_file.read(),
        #   password=password,
        # )
        public_key = serialization.load_pem_public_key(
            key_file.read(),
        )
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    try:
        ## BUG: may obliterate private-key when it already exists
        user_db.save_key(
            alias=alias,
            fingerprint=hashlib.sha256(public_bytes).hexdigest(),
            priv_bytes=None,
            pub_bytes=public_bytes
        )
    except:
        print(repr(sys.exception()))

def query_export_public_key(fp: str):
    '''export public key to a specific location'''
    rowdata = user_db.get_row_by_fp(fp)
    if not rowdata:
        # cys_console("///row-data is None///")
        return
    name = rowdata[0] + ".public_key.pem"
    public_bytes_der = rowdata[3] # public-key blob already
    
    public_key = serialization.load_der_public_key(public_bytes_der)

    file_path = file_path_picker(name)
    if file_path:
        # TODO: loading bar
        with open(file_path, "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        # cys_console("save file to: ", file_path)

    

# if __name__ == "__main__":
    # openpgp_encrypt(public_key=public_key)
    # openpgp_decrypt(private_key=private_key)
    # create_key_pairs("test1919810")
