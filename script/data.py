import json
import os
from pathlib import Path
from script.db import KeyDatabase

setting_list = ["check1", "check2", "check3", "check4"]
json_data = {item : 0 for index, item in enumerate(setting_list)}

# test code
if __name__ == "__main__":
    print("\nTest: data")
    print(json_data)
    for k in json_data:
        print(k, json_data[k])

## json for setting
'''
Python executes A.py completely the first time it is imported.
By the time B.py looks at X, the with open block has already finished.

Python modules are cached.
This means if you import A in ten different files, Python only runs the code in A.py once.
'''
if os.path.exists("settings.json"):
    with open("settings.json", "r") as f:
        saved_data = json.load(f)
        print("Loading saved setting...", saved_data)
        for key in json_data:
          if saved_data.get(key):
            json_data[key] = saved_data[key]
        print("Loading complete", json_data)

def update_json(data):
    with open("settings.json", "w") as f:
      json.dump(data, f)
    print("Local files have been updated.")

# completely synchronous (a synchronous file system, amazing!)
if __name__ == "__main__":
  print(json_data)
  for i, v in enumerate(json_data):
    print(i, v)

## SQLite for users (a user is a stored public key or key pairs)
no_user = False
home_dir = Path.home() / ".cypherstone" # C:\Users\{current user}\.cypherstone
# userindex_json = home_dir / "index.json"
# if userindex_json.exists():
#   with open(userindex_json) as f:
#     saved_user = json.load(f)
#     print("Loading saved user...", saved_user)
# else:
#   home_dir.mkdir(parents=True, exist_ok=True)
#   no_user = True
#   print("no user")

user_db = KeyDatabase(home_dir / "keys_storage.db")
print(f"User list: {user_db.list_all_aliases()}")
if len(user_db.list_all_aliases()) == 0:
  no_user = True

# print("result", user_db.list_all_table_data())