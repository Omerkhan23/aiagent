import os

def write_file(working_directory: str , file_path:str , content:str ) -> str:

    abs_path_WD = os.path.abspath(working_directory)

    target_file_path = os.path.normpath(os.path.join(abs_path_WD,file_path))
    
    valid_file_path = os.path.commonpath([abs_path_WD,target_file_path]) == abs_path_WD

    if not valid_file_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    elif os.path.isdir(target_file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    else:
        try:
            os.makedirs(os.path.dirname(target_file_path),exist_ok=True)
            with open(target_file_path,"w") as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            return f"Error: {e}"
        
       

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file (and any necessary parent directories) if it does not already exist, or overwrites it if it does.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)