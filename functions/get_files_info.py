import os
def get_files_info(working_directory, directory="."):
    # Obtain the absolute paths of needed files and directories
    full_directory = os.path.join(working_directory, directory)
    abs_wd_path = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_directory)

    # print("\n".join([full_directory,abs_wd_path,abs_d_path,abs_full_path]))

    # Asserts that directory is inside working directory
    if not abs_full_path.startswith(abs_wd_path):
        print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        return

    # Asserts that full path exists
    if not os.path.exists(abs_full_path):
        print(f'Error: "{directory}" is not a directory')
        return
    
    # Iterate over each found item inside full path and list its information.
    list_contents = os.listdir(abs_full_path)
    for item in list_contents:
        item_path = os.path.join(abs_full_path, item)
        size = os.path.getsize(item_path)
        is_dir = os.path.isdir(item_path)
        print(f"- {item}: file_size={size} bytes, is_dir={is_dir}")