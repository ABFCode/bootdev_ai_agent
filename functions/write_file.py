import os

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = abs_working_dir

    if file_path:
        target_file = os.path.join(abs_working_dir, file_path)
    
    parent_dir = os.path.dirname(target_file)
    if not os.path.exists(parent_dir):
        try:
            os.makedirs(parent_dir)
        except Exception as e:
            return f"Error: error making directories: {e}"
    
    try:
        with open(target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: error writing to file: {target_file}, {e}"