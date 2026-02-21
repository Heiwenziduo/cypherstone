from cryptography.fernet import Fernet

def generate_key():
  """Generates a key and saves it to a file"""
  key = Fernet.generate_key()
  with open("secret.key", "wb") as key_file:
    key_file.write(key)
  print("Key generated and saved as 'secret.key'. Keep this safe!")

def encrypt_message(message):
  """Encrypts a simple string"""
  with open("secret.key", "rb") as key_file:
    key = key_file.read()
  
  f = Fernet(key)
  encrypted_message = f.encrypt(message.encode())
  print(f"Encrypted: {encrypted_message.decode()}")
  return encrypted_message

# # Let's test the logic
# if __name__ == "__main__":
#     print(f"--- Welcome to {bold}CypherStone{bold} ---")
#     generate_key()
#     encrypt_message("This is a top secret Windows file!")