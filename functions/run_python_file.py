import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_file = os.path.join(abs_working_dir, file_path)
    abs_abs_target_file = os.path.abspath(abs_target_file)

    if not abs_abs_target_file.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_target_file):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result: subprocess.CompletedProcess = subprocess.run(["python3", abs_target_file], timeout=30, capture_output=True, cwd=abs_working_dir)
        out = result.stdout.decode(encoding='utf-8')
        err = result.stderr.decode(encoding='utf-8')

        stdout = f"STDOUT: {out}"
        stderr = f"STDERR: {err}"
        exit_code = result.returncode
        
        if not out.strip() and not err.strip():
            return "No output produced"
        
        if exit_code != 0:
            return stdout + stderr + f"Process exited with error code: {exit_code}"
        else:
            return stdout + stderr
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="run a specific python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the python file to run, relative to the working directory.",
            ),
        },
    ),
)