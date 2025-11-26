import os
from google.genai import types
from config import MAX_CHARS
def get_file_content(working_directory, file_path):
    abs_wd_path = os.path.abspath(working_directory)
    abs_fl_path = os.path.abspath(os.path.join(abs_wd_path, file_path))

    # Assert that file inside is inside working_directory
    if not abs_fl_path.startswith(abs_wd_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # Asserts that file is in fact a file and not a directory:
    if not os.path.isfile(abs_fl_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    # Use the constant in config.py for max characters
    # Open the file as "read"
    with open(abs_fl_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)
        if len(file_content_string) >= MAX_CHARS:
            file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
        return file_content_string
    
# Schema will allow the model to run this function
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists the files content constrained to the working directory. If the file has more than MAX_CHAR characters, it gets truncated",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file for which the contents are needed. Path is relative to the provided working directory",
            ),
        },
    ),
)