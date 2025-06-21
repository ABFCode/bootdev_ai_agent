import os
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = abs_working_dir

    if file_path:
        target_file = os.path.join(abs_working_dir, file_path)

    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        f'Error: File not found or is not a regular file: "{file_path}"'
    
    MAX_CHARS = 10000

    try:
        with open(target_file, "r") as f:
            file_content = f.read(MAX_CHARS)
            if len(file_content) == MAX_CHARS:

                return file_content + f"...File {file_path} truncated at 10000 characters"
            return file_content
    except Exception as e:
        return f"Error listing files: {e}"
    


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the string contents of a specific file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to get file content from, relative to the working directory.",
            ),
        },
    ),
)