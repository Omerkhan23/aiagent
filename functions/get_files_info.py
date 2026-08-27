import os

from google.genai import types

def get_files_info(working_directory: str, directory: str = ".") -> str:

    #getting the absolute path of the working directory
    absolute_path_WD = os.path.abspath(working_directory)

    #joining it with the directory path to get the full path
    target_dir = os.path.normpath(os.path.join(absolute_path_WD, directory))

    #checking whether commonpath is same for both WD and diectory
    valid_target_dir = os.path.commonpath([absolute_path_WD,target_dir]) == absolute_path_WD
    result = f"Result for '{directory}' directory:\n"
    if not valid_target_dir:
        return f'   Error: Cannot list "{directory}" as it is outside the permitted working directory'
    # checking whethter the directory is directory not a file
    elif not os.path.isdir(target_dir):
        return f'   Error: "{directory}" is not a directory'
    
    else:
        target_dir_items = os.listdir(target_dir)
        
        for item in target_dir_items:
            item_path = os.path.normpath(os.path.join(target_dir,item))
        
            result += f"   - {item}: file_size={os.path.getsize(item_path)}, is_dir={os.path.isdir(item_path)}\n"

        return result.strip()
    
#schema to define the the function for LLM 
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

    



    


