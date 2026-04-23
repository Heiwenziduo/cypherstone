import os
from tkinter import filedialog

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet

from script.data import validate_file_path
from script.errors import CryptoError

# encrypted file suffix
_suffix = ".cys"
'''.cys encrypted file suffix'''
#
_separator = b"---SEP---"

## =========================================================================================
def openpgp_encrypt(public_key, input_file_path: str, output_file_path: str = ""):
  '''use public key to encrypt a file'''
  if not validate_file_path(input_file_path):
    raise CryptoError("Invalid File Path")
  
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

  # 5. Save the result (This is .pgp style file)
  output_path = output_file_path if output_file_path else input_file_path
  with open(f"{output_path}{_suffix}", "wb") as f:
    f.write(encrypted_session_key + _separator + encrypted_data)


## =========================================================================================
def openpgp_decrypt(private_key, input_file_path: str, output_file_path: str = ""):
  '''private key to decrypt'''
  if not validate_file_path(input_file_path):
    raise CryptoError("Invalid File Path")
    
  with open(input_file_path, "rb") as f:
    file_data = f.read()

  if _separator not in file_data:
    raise CryptoError("Invalid File Format")

  encrypted_session_key, encrypted_file_data = file_data.split(_separator, 1)
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

  output_path = output_file_path if output_file_path else input_file_path.removesuffix(_suffix)
  with open(f"{output_path}", "wb") as f:
    f.write(decrypted_data)
  # print("Success! File has been decrypted: ", output_path)

# def browse_file():
#   filename = filedialog.askopenfilename(
#     initialdir=os.path.expanduser("~/Documents")
#   )
#   print(filename)
#   return filename
