import shutil

# Example usage
# source_directory = '/path/to/source'
# destination_directory = '/path/to/destination'
# copy_files_recursive(source_directory, destination_directory)
def copy_files_recursive(source_dir, destination_dir, debug=False):
    """
    Recursively copy all files and folders from the source directory to the destination directory.

    Args:
        source_dir (str): Path to the source directory.
        destination_dir (str): Path to the destination directory.
    """
    try:
        shutil.copytree(source_dir, destination_dir, dirs_exist_ok=True)
        if debug:
          print(f"Files and folders copied from {source_dir} to {destination_dir} successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def file_replace_text(file_text, old_text, new_text, mode='replace'):
    with open(file_text, 'r') as file:
        lines = file.readlines()

    with open(file_text, 'w') as file:
        for line in lines:
            if old_text in line:
                if mode == 'replace':
                    line = line.replace(old_text, new_text)
                if mode == 'append':
                    line = line.strip() + new_text
                    
            file.write(line)
            
def file_append(file_path, text):
    with open(file_path, 'a') as file:
        file.write(text)

def file_write(file_path, text):
    with open(file_path, 'w') as file:
        file.write(text)
        
def file_read(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
    return file_content