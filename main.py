import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions
from functions.call_function import call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)


    verbose = "--verbose" in sys.argv

    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("Wrong")
        sys.exit(1)

    user_prompt = " ".join(args)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    if verbose:
        print(f"User prompt: {user_prompt}")
    
    generate_content(client, messages, verbose)



def generate_content(client, messages, verbose):

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions])
    )

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if not response.function_calls:
        return response.text
    
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        function_call_result = call_function(function_call_part, True)

        if not function_call_result.parts[0].function_response.response:
            raise Exception("Bad function response")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
    

if __name__ == "__main__":
    main()