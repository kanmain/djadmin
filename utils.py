import os
import re

import settings

from Lib.venv import (
    venv_run, venv_get_current_script_path
  )
from Lib.folder import folder_create
from Lib.file import (
    copy_files_recursive, file_replace_text
  )
venv_path = '. /mnt/data/work/apps/djadmin/.venv/bin/activate'

def inputs(prompt, default=None):
  full_prompt = f"{prompt} [{default}]: "
  user_input = input(full_prompt)
  if not user_input.strip() and default is not None:
    return default
  return user_input

def ask_main_folder():
  main_folder = inputs("Input main folder: ", "be")
  config_folder = inputs("Input config folder: ", "config")
  return main_folder, config_folder
  
def create_django_project():
  main_folder, config_folder = ask_main_folder()
  
  if config_folder:
    result = 0
    
    if main_folder != ".":
      result = os.system(f"mkdir {main_folder}")

    if result == 0:
      cmd = f"django-admin startproject {config_folder} {main_folder}"
      result = venv_run(venv_path=venv_path, cmd=cmd)
      if result == 0:
        print(f"Django project {main_folder}/{config_folder} is successfully created.")
        # 
  else:
      print("Config folder cannot be empty.")

def config_settings():
  main_folder, config_folder = ask_main_folder()
  config_path = f'{main_folder}/{config_folder}'
  
  
  # Create folder settings
  settings_folder = f'{config_path}/settings'
  result = folder_create(settings_folder)
  
  # Copy template from assets
  source_directory = f'{settings.BASE_DIR}/assets'
  destination_directory = f'{os.getcwd()}/{main_folder}'
  copy_files_recursive(source_directory, destination_directory)
  
  # Copy file .env.sample to .env
  result = os.system(f"mv {main_folder}/.env.sample {main_folder}/.env")
    
  # Move settings.py to config/settings/base.py
  result = os.system(f"mv {config_path}/settings.py {settings_folder}/base.py")
  
  # Membaca SECRET_KEY dari settings.py
  base_file = f"{settings_folder}/base.py"
  with open(base_file, "r") as settings_file:
    base_content = settings_file.read()
    # secret_key = settings_content.split("SECRET_KEY = '")[1].split("'")[0]
  
  # Use regular expression to extract the value of SECRET
    secret_match = re.search(r'SECRET_KEY\s*=\s*\'(.*?)\'', base_content)
    if secret_match:
        secret_value = secret_match.group(1)
        # Replace SECRET with an empty string
        processed_content = base_content.replace(secret_value, '')
        
        # Write back the processed content to the base.py file
        with open(base_file, 'w') as base_file:
            base_file.write(processed_content)
        
        # Write to .env
        file_env = f'{main_folder}/.env'
        result = file_replace_text(file_text=file_env, old_text='SECRET_KEY =', new_text=f'SECRET_KEY = {secret_value}')
    
  return result
    







# def modify_settings_and_move_secret_key():
#     main_folder = inputs("Masukkan folder project Django: ")
#     config_folder = inputs("Masukkan folder settings project Django: ", "config")

#     if not os.path.isdir(main_folder):
#         print(f"Project folder '{main_folder}' tidak ditemukan.")
#         return

#     # Membaca SECRET_KEY dari settings.py
#     with open(f"{main_folder}/{config_folder}/settings.py", "r") as settings_file:
#         settings_content = settings_file.read()
#         secret_key = settings_content.split("SECRET_KEY = '")[1].split("'")[0]

#     # Memindahkan SECRET_KEY ke file .env
#     with open(f"{main_folder}/.env", "w") as env_file:
#         env_file.write(f"SECRET_KEY = '{secret_key}'")

#     # Menghapus SECRET_KEY dari settings.py
#     with open(f"{main_folder}/{config_folder}/settings.py", "w") as settings_file:
#         settings_file.write(
#             settings_content.replace(
#                 f"SECRET_KEY = '{secret_key}'", "SECRET_KEY = config('SECRET_KEY')"
#             )
#         )

#     with open(f"{main_folder}/{config_folder}/settings.py", "r+") as file:
#         content = file.read()
#         file.seek(0, 0)  # Pindah kursor ke awal berkas
#         file.write(
#             f"from decouple import config, Csv\n\n{content}"
#         )  # Menulis teks baru diikuti oleh isi berkas yang lama

#     print("SECRET_KEY telah dipindahkan ke file .env.")

