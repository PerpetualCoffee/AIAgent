import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("API_KEY not found!")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="Please enter your single-line prompt.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access 'args.user_prompt'

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature=0),
    )

    function_results = []

    if response.usage_metadata is None:
        raise RuntimeError("the API request has failed!")
    else:
        if args.verbose:
            print(F"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if response.function_calls is not None:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=args.verbose)
                if not function_call_result.parts:
                    raise Exception("function_call_result.parts is empty")
                if function_call_result.parts[0].function_response is None:
                    raise Exception("function_response is None")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("function_response.response is None")

                function_results.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print(f"Response:\n{response.text}")


if __name__ == "__main__":
    main()
