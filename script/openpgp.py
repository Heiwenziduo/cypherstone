import os
from tkinter import filedialog

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.fernet import Fernet

# encrypted file suffix
_suffix = ".cys"
'''.cys encrypted file suffix'''
#
_separator = b"---SEP---"

## use public key to encrypt a file
def openpgp_encrypt(public_key, file_path: str):
  # 1. Generate a random Symmetric key (The "Session Key")
  session_key = Fernet.generate_key()
  cipher_aes = Fernet(session_key)

  # 2. Read your file as bytes
  # filename = browse_file()
  # if not os.path.exists(filename):
  #   print("not exist")
  #   return
  with open(file_path, "rb") as f:
    file_data = f.read()

  # 3. Encrypt the file data
  encrypted_data = cipher_aes.encrypt(file_data)

  # 4. Encrypt the Session Key using your Public Key
  encrypted_session_key = public_key.encrypt(
    session_key,
    padding.OAEP(
      mgf=padding.MGF1(algorithm=hashes.SHA256()),
      algorithm=hashes.SHA256(),
      label=None
    )
  )

  # 5. Save the result (This is your .pgp style file)
  with open(f"{file_path}{_suffix}", "wb") as f:
    f.write(encrypted_session_key + _separator + encrypted_data)

## private key to decrypt
def openpgp_decrypt(private_key):
  filename = browse_file()
  if not os.path.exists(filename):
    print("not exist")
    return
  with open(filename, "rb") as f:
    file_data = f.read()

  if _separator not in file_data:
    print("Error: Invalid file format (no separator found).")
    return

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
      return

  cipher_aes = Fernet(session_key)
  try:
    decrypted_data = cipher_aes.decrypt(encrypted_file_data)
  except Exception:
    print("Error: The file data is corrupted or the session key is incorrect.")
    return

  rawname = filename.removesuffix(_suffix)
  with open(f"{rawname}", "wb") as f:
    f.write(decrypted_data)
  print("Success! File has been decrypted: ", rawname)

def browse_file():
  filename = filedialog.askopenfilename(
    # initialdir=os.path.expanduser("~/Documents")
  )
  print(filename)
  return filename
