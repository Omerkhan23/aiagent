import os
from google.genai import types

def get_files_info(working_directory , directory = '.'):

    full_path = os.path.join(working_directory , directory)

    abs_full_path = os.path.abspath(full_path)

    working_directory = os.path.abspath(working_directory)

    if not abs_full_path.startswith(working_directory + os.sep) and abs_full_path != working_directory:

        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    elif not os.path.isdir(abs_full_path):

        return f'Error: "{directory}" is not a directory'

    else:

        file_path = os.listdir(abs_full_path)

        result = f"Result for current directory:\n"

        for filename in file_path:
            complete_filepath = os.path.join(abs_full_path,filename)
            file_size = os.path.getsize(complete_filepath)
            is_dir  = os.path.isdir(complete_filepath)

            result += f" - {filename}: file_size={file_size} bytes,is_dir={is_dir}\n"

        return result.strip()

    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

    
