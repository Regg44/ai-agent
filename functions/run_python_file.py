import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_wd_path = os.path.abspath(working_directory)
    abs_fl_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Ensure file is inside working directory
    if not abs_fl_path.startswith(abs_wd_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    # Ensure file exists
    if not os.path.exists(abs_fl_path):
        return f'Error: File "{file_path}" not found.'
    # Ensure file ends with .py
    if not abs_fl_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    # Execute python file, catching any errors that might come up
    try:
        thin = subprocess.run(["python", abs_fl_path, *args], 
                              timeout=30, 
                              cwd=abs_wd_path,
                              capture_output=True,
                              text=True)
        if thin.stdout == None:
            return "No output produced"
        
        result_message = f"STDOUT: {thin.stdout}", f"STDERR: {thin.stderr}"
        if thin.returncode != 0:
            result_message += f"\nProcess exited with code {thin.returncode}"
        return result_message
    except Exception as e:
        return f"Error: executing Python file: {e}"

# Schema will allow model to run this function
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the python file constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the .py file to be executed. Path is relative to the provided working directory",
            )
        },
    ),
)