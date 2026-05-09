import os
from tkinter import filedialog

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet

from script.errors import CryptoError
from script.data import user_db
from script.constants import c_default_passphrase, c_file_suffix
#
_separator = b"---SEP---"

## =========================================================================================
def openpgp_encrypt(fp: str, input_file_path: str, output_file_path: str = ""):
  '''use public key to encrypt a file'''
  if not validate_file_path(input_file_path):
    raise CryptoError("Invalid File Path")
  
  public_key = get_public_key_by_fp(fp)
  if not isinstance(public_key, rsa.RSAPublicKey):
    raise CryptoError("Invalid Public Key")
  
  # 1. Generate a random Symmetric key (The "Session Key")
  session_key = Fernet.generate_key()
  cipher_aes = Fernet(session_key)

  # 2. Read file as bytes
  with open(input_file_path, "rb") as f:
    file_data = f.read()

  # 3. Encrypt the file data
  encrypted_data = cipher_aes.encrypt(file_data)

  # 4. Encrypt the Session Key using Public Key
  encrypted_session_key = public_key.encrypt(
    session_key,
    padding.OAEP(
      mgf=padding.MGF1(algorithm=hashes.SHA256()),
      algorithm=hashes.SHA256(),
      label=None
    )
  )

  # 5. Save the result with 3 parts: FINGERPRINT ---SEP--- SESSION_KEY ---SEP--- DATA
  output_path = output_file_path if output_file_path else input_file_path + c_file_suffix
  with open(f"{output_path}", "wb") as f:
    f.write(fp.encode() + _separator + encrypted_session_key + _separator + encrypted_data)


## =========================================================================================
def openpgp_decrypt(input_file_path: str, output_file_path: str = ""):
  '''private key to decrypt'''
  if not validate_file_path(input_file_path):
    raise CryptoError("Invalid File Path")
    
  with open(input_file_path, "rb") as f:
    file_data = f.read()

  parts = file_data.split(_separator, 2)
  if len(parts) != 3:
      raise CryptoError("Invalid or Corrupted File Format") # not for CypherStone

  fp_bytes, encrypted_session_key, encrypted_file_data = parts
  fp_string = fp_bytes.decode()
  private_key = get_private_key_by_fp(fp_string)
  if not isinstance(private_key, rsa.RSAPrivateKey):
      '''Only RSA keys can encrypt and decrypt data. The other types can only be used for "Signing"'''
      raise CryptoError("Invalid key type: Expected an RSA Private Key.")
  try:
    session_key = private_key.decrypt(
      encrypted_session_key,
      padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
      )
    )
  except Exception as e:
      print(f"Decryption failed! Likely the wrong private key or password. Error: {e}")
      raise CryptoError("Missing Private Key")

  cipher_aes = Fernet(session_key)
  try:
    decrypted_data = cipher_aes.decrypt(encrypted_file_data)
  except Exception as e:
    print("Error: The file data is corrupted or the session key is incorrect.")
    raise CryptoError("Corrupted Session Key")

  output_path = output_file_path if output_file_path else input_file_path.removesuffix(c_file_suffix)
  with open(f"{output_path}", "wb") as f:
    f.write(decrypted_data)
  # print("Success! File has been decrypted: ", output_path)

def validate_file_path(file_name: str) -> bool:
    '''check whether the path is authentic'''
    return os.path.exists(file_name)


##
def get_public_key_by_fp(fp: str):
    ''''''
    # TODO: empty fp always fetches the first row
    rowdata = user_db.get_row_by_fp(fp)
    if not rowdata:
        # cys_console("Can not get data. Invalid finger-print.")
        # TODO: throwing an exception and catching that at console screen maybe better.
        return
    alias = rowdata[0]
    finger_print = rowdata[1]
    public_bytes_der = rowdata[3]
    print(f"fp: {fp}")
    print(f"User {alias} has got the public key.")
    '''
    If your bytes are raw binary (often how they are stored in SQLite for efficiency),
    you cannot just name the file .pem.
    You must first turn them back into a Public Key object and then "export" them as PEM.
    '''
    public_key = serialization.load_der_public_key(public_bytes_der)
    '''
    PEM (.pem): It is "Human Readable."
    You can open it in Notepad and see the headers. This is great for sharing keys with other people or systems.

    DER/Bytes: It is "Machine Readable."
    It takes up less space and is faster for a database like SQLite to process
    because it doesn't have to deal with text encoding.
    '''
    # return (alias, finger_print, public_key)
    return public_key

def get_private_key_by_fp(fp: str):
    """Retrieves and unlocks the private key for the given fingerprint."""
    rowdata = user_db.get_row_by_fp(fp)
    
    # Check if user exists and actually has a private key (not just a public one)
    if not rowdata or not rowdata[2]: 
        raise CryptoError("Private key not found for this identity.")
        
    private_bytes_pem = rowdata[2]
    
    try:
        # Deserialize using the default passphrase 
        private_key = serialization.load_pem_private_key(
            private_bytes_pem,
            password=c_default_passphrase
        )
        return private_key
    except Exception as e:
        raise CryptoError(f"Failed to unlock private key: {e}")
