import os
from google.genai import types
from config import MAX_CHARS
def get_file_content(working_directory:str , file_path:str) -> str:

    absolute_path_WD = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(absolute_path_WD, file_path))
    valid_file_path = os.path.commonpath([absolute_path_WD,target_file]) == absolute_path_WD
    
    if not valid_file_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    else:
        try:
            with open(target_file,"r") as f:
                file_content_string = f.read(MAX_CHARS)
                if f.read(1) :
                    file_content_string += (f'[...File "{file_path}" truncated at {MAX_CHARS} characters]')

            return file_content_string
        
        except Exception as e:
            return f"Error reading file: {file_path}: {e}"
        
schema_get_file_content = types.FunctionDeclaration(
    name = 'get_file_content',
    description='Reads the content of a file within the working directory. If the file exceeds the maximum allowed characters, the content is truncated and a truncation notice is appended.',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            'file_path': types.Schema(
                type=types.Type.STRING,
                description='The path to the file to read, relative to the working directory.'
            )
        },
    required=['file_path']
    )

)



