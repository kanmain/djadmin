import os
import re

import settings

from Lib.venv import (
    venv_run
  )
from Lib.folder import folder_create
from Lib.file import (
    copy_files_recursive, file_replace_text, file_append, file_read, file_write
  )

venv_path = '. /mnt/data/work/apps/djadmin/.venv/bin/activate'

'''
Inputs
'''
def inputs(prompt, default=None):
  full_prompt = f"{prompt} [{default}]: "
  user_input = input(full_prompt)
  if not user_input.strip() and default is not None:
    return default
  return user_input

'''
Ask main folder
'''
def ask_main_folder():
  main_folder = inputs("Input main folder: ", "be")
  config_folder = inputs("Input config folder: ", "config")
  return main_folder, config_folder


'''
Create Django project
'''
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

'''
Config Settings
'''
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
    

'''
Start Django app
'''
def start_django_app():
  app_name = inputs('Input app name:')  
  
  if app_name:
    main_folder, config_folder = ask_main_folder()
    prefix_table = inputs('Input prefix table', 'be')
    add_to_env = inputs('Add to .env', 'Yes')

    # Check folder exist
    folder_app = f'{main_folder}/{settings.APP_DIR}/{app_name}'
    result = folder_create(path=folder_app)
    
    # Create django app
    command = f'django-admin startapp {app_name} {folder_app}'
    result = venv_run(venv_path=venv_path, cmd=command)
    
    if result == 0:
      # Modify app_name/apps.py
      file_apps = f'{folder_app}/apps.py'
      result = file_replace_text(file_text=file_apps, 
                                old_text=f"name = '{app_name}'", 
                                new_text=f"name = '{settings.APP_DIR}.{app_name}'")
      
      # Append User models
      template_models = f'{settings.BASE_DIR}/templates/models.py'
      text = file_read(template_models)
      # Replace Xmodel
      text = text.replace('Xmodel', app_name.capitalize()).replace('x_xmodel', f'{prefix_table}_{app_name}')
      # Append to apps/models.py
      file_models = f'{folder_app}/models.py'
      result = file_write(file_path=file_models, text=text)
      
      if add_to_env == 'Yes':
        # Append to .env
        file_env = f'{main_folder}/.env'
        text = 'CUSTOM_APPS = '
        new_text = f' {settings.APP_DIR}.{app_name}, \n'
        file_replace_text(file_text=file_env, old_text=text, new_text=new_text, mode='append')
        
        # Append to be/config/urls.py
        # path('', include(('apps.users.urls', 'users'), namespace='users')),
        file_urls = f'{main_folder}/{config_folder}/urls.py'
        text = "path('admin/', admin.site.urls),"
        new_text = f"\n\n\tpath('{app_name}/', include(('{settings.APP_DIR}.{app_name}.urls', '{app_name}'), namespace='{app_name}')),\n\n"
        file_replace_text(file_text=file_urls, old_text=text, new_text=new_text, mode='append')
        
        
      
      # Views
      template_views = f'{settings.BASE_DIR}/templates/views.py'
      text = file_read(template_views)
      # replace
      text = text.replace('XView', f'{app_name.capitalize()}View').replace('xviews.html', f'{app_name}.html')
      file_views = f'{main_folder}/{settings.APP_DIR}/{app_name}/views.py'
      result = file_write(file_path=file_views, text=text)
      
      # Copy templates/views.py & urls.py
      folder_template = f'{folder_app}/templates'
      result = folder_create(path=folder_template)
      result = os.system(f"cp {settings.BASE_DIR}/templates/views.html {folder_app}/templates/{app_name}.html")
      
      # Urls
      template_urls = f'{settings.BASE_DIR}/templates/urls.py'
      text = file_read(template_urls)
      # replace
      text = text.replace('XView', f'{app_name.capitalize()}View').replace('xname', app_name)
      file_urls = f'{main_folder}/{settings.APP_DIR}/{app_name}/urls.py'
      result = file_write(file_path=file_urls, text=text)
      
      
      print(f'Creating app "{folder_app}" success...')
    
    # Modify app_name/apps.py
    





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

