import os
import subprocess
from google.genai import types
from config import WORKING_DIR
# Imports of available functions
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file

# Map function names to functions themselves:
function_mappings = {
    "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file
}
# Function to call other functions
def call_function(function_call_part: types.FunctionCall, verbose=False, f_map=function_mappings):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    # Run function
    # Ensure its mapped first
    if function_call_part.name in f_map:
        r_func=f_map[function_call_part.name]
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    try:  
        function_response = r_func(working_directory=WORKING_DIR, **function_call_part.args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": function_response}
                )
            ]
        )
    except Exception as e:
        return f"Error: {e}"