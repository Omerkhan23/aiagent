
import os
import subprocess

#Run the pyhton file and return the result
def run_python_file(working_directory:str ,file_path:str ,args:list[str]|None = None) -> str:

    absolute_path_WD = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(absolute_path_WD,file_path))
    valid_target_file = os.path.commonpath([absolute_path_WD,target_file]) == absolute_path_WD

    if not valid_target_file:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    elif not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    else:
        try: 
            command = ["python" , target_file]
            if args:
                command.extend(args)

            result = subprocess.run(command,
                                    capture_output=True,
                                    text=True,
                                    timeout=30,
                                    )
            returncode = result.returncode
            if returncode != 0:
                return f"Process exited with code {returncode}\nSTDOUT:{result.stdout}\nSTDERR:{result.stderr}"
            elif not result.stdout and not result.stderr:
                return f"No output prooduced"
            
            return f"STDOUT:{result.stdout} , STDERR:{result.stderr}"
        except subprocess.SubprocessError as e:
            return f"Subprocess error: {e}"
        
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)

            
