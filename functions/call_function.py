from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file


def call_function(function_call_part: types.FunctionCall, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    print(f" - Calling function: {function_call_part.name}")

    function_name = function_call_part.name
    if function_name not in ["get_file_content", "get_files_info", "run_python_file", "write_file"]:
        print(" func name: " + function_name)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    function_args = function_call_part.args

    if function_name == "get_files_info":
        result = get_files_info("./calculator", **function_args)
    elif function_name == "get_file_content":
        result = get_file_content("./calculator", **function_args)
    elif function_name == "run_python_file":
        result = run_python_file("./calculator", **function_args)
    elif function_name == "write_file":
        result = write_file("./calculator", **function_args)

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": result},
        )
    ],
)