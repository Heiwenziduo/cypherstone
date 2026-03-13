import json
import os
from pathlib import Path
from tkinter import filedialog
from gui.console_screen import cys_console
from script.db import KeyDatabase
from cryptography.hazmat.primitives import serialization

# --- GLOBAL INTERFACE ---
_current_user_fp: str = ""
def current_user_fp():
  return _current_user_fp

# def current_user_alias():
#   row = user_db.get_row_by_fp(_current_user_fp)
#   return row[0] if row else ""

setting_list = ["check1", "check2", "check3", "check4"]
json_data = {item : 0 for index, item in enumerate(setting_list)}

## utilities
def file_path_picker(file_name=None):
    '''when file_name is given, use save-file dialog'''
    if not file_name:
      # try: # hide logs in console
      file_path = filedialog.askopenfilename(
          title="Select a file for CypherStone",
          # initialdir=os.path.expanduser("~/Documents")
      )
    else:
      file_path = filedialog.asksaveasfilename(
          title="Save your files",
          initialfile=file_name,
          # defaultextension=".pem",
      )
      # cys_console("save file to: ", file_path)
    return file_path

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
        # print("Loading saved setting...", saved_data)
        for key in json_data:
          if saved_data.get(key):
            json_data[key] = saved_data[key]
        # print("Loading complete", json_data)

def update_json(data):
    with open("settings.json", "w") as f:
      json.dump(data, f)
    print("Local settings files have been updated.")

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

## completely synchronous (a synchronous file system, amazing!)
if __name__ == "__main__":
  print(json_data)
  for i, v in enumerate(json_data):
    print(i, v)