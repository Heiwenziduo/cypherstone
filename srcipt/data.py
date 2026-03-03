import json
import os

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

# completely synchronous
if __name__ == "__main__":
  print(json_data)
  for i, v in enumerate(json_data):
    print(i, v)

## SQLite for users