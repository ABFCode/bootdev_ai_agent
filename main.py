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

    if verbose:
        print(f"User prompt: {user_prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    MAX_ITERS = 20
    
    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations reached")
            sys.exit(1)
        
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final responses:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")



def generate_content(client, messages, verbose):
    
    response: types.GenerateContentResponse = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions])
    )
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    
    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)
    
    if not response.function_calls:
        return response.text
    
    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if(
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("Empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])
    
    if not function_responses:
        raise Exception("No function responses generated, exiting")
    
    messages.append(types.Content(role="tool", parts=function_responses))


if __name__ == "__main__":
    main()


            
        

if __name__ == "__main__":
    main()