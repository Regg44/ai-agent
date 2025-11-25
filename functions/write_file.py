import os

def write_file(working_directory, file_path, content):
    # Obtain the absolute path of relevant files and directories.
    abs_wd_path = os.path.abspath(working_directory)
    abs_fl_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Check file inside the working directory
    if not abs_fl_path.startswith(abs_wd_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        file_parameters = "w"
        # If file doesn't exist, create it, add "x" to argument to create file
        if not os.path.exists(abs_fl_path):
            file_parameters = "x"
        
        with open(abs_fl_path, file_parameters) as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

