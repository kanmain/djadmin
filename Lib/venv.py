import os
import subprocess


def venv_run(venv_path, cmd):
  # activate_script = os.path.join(venv_path, 'bin', 'activate')
  # print(activate_script)
  
  # Check if the activation script exists
  result = -1
  # if os.path.exists(venv_path):
  command = f"{venv_path} && {cmd}"
  result = subprocess.call(command, shell=True)
  # print(f'Command: {command}\nResult: {result}\n')
  # else:
  #   print(f"Virtual environment '{activate_script}' not found.")

  return result

def venv_get_current_script_path():
    """
    Get the path of the currently executing Python script.
    """
    return os.path.abspath(__file__)