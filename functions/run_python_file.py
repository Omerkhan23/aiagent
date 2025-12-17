import os

import subprocess
import sys
from google.genai import types

def run_python_file(working_directory, file_path, args=None):

    working_directory_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory_path, file_path))

    if not (abs_file_path == working_directory_path or abs_file_path.startswith(working_directory_path + os.sep)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    elif not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    else:
        try:
            timeout = 30
            # Build command to run the target Python file with the current Python interpreter.
            # - sys.executable is the path to the interpreter running this process (e.g., '/usr/bin/python3').
            # - abs_file_path is the absolute path to the .py file to execute.
            # - args is an optional list of additional CLI arguments; use an empty list when None.
            cmd = [sys.executable, abs_file_path] + (args or [])
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
                cwd=working_directory_path
            )

            if result.returncode != 0:
                return f'Process exited with code {result.returncode} , STDOUT:{result.stdout} , STDERR:{result.stderr}'
            if not result.stdout.strip() and not result.stderr.strip():
                return "Error: No output produced"
            return f'STDOUT:{result.stdout} , STDERR:{result.stderr}'
        except subprocess.TimeoutExpired:
            return "Error: No output is produced - Process timed out"
        except Exception as e:
            return f"Error: executing Python file: {e}"
        
schema_run_python_file = types.FunctionDeclaration(
    name = 'run_python_file',
    description='runs the python file with optional arguements'
    parameters=types.Schema(
        type = types.Type.OBJECT,
        properties = {
            ''
        }
    )
    
)