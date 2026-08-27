from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_file_content  import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

# Mapping callables functions to strings for LLM to follow in a dict
function_map = {
    "get_files_info": get_files_info,
    "get_file_content":get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}


def call_function(function_call_part: types.FunctionCall, verbose:bool = False) -> types.Content:
    function_name = function_call_part.name
    function_args = dict(function_call_part.args) if function_call_part.args else {}

    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" -Calling function: {function_name}")

    if function_name is None:# i:e not in function_map
        return types.Content(
            role="user",
            parts=[
                types.Part.from_function_response(
                    name="Unknown function",# This part will run if we the function is not present i:e None
                    response={f"Error": f"Unknown function: {function_name}"},)#wrote error in dict form as it is required by gemini sdk
            ],
        )
    #Inject working directory by ourselves LLM doesn't know about it
    function_args["working_directory"] = "./calculator"

    function_to_call = function_map[function_name]
    result = function_to_call(**function_args)

    return types.Content(
        role="user",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )

