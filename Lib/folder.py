import os 

def folder_create(path):
  folders = path.split("/")
  current_path = ""
  result = -1
  for folder in folders:
    current_path = os.path.join(current_path, folder)
    if not os.path.exists(current_path):
      result = os.makedirs(current_path)
  return result 