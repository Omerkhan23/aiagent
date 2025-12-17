def main():
    import os
    import sys
    from dotenv import load_dotenv
    from google import genai
    from google.genai import types
    from functions.get_files_info import schema_get_files_info
    from functions.get_file_content import schema_get_file_content

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client  =genai.Client(api_key=api_key)

    available_functions = types.Tool(
            function_declarations=[schema_get_files_info , schema_get_file_content],)
    
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. 
    You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    
    verbose = False
    if len(sys.argv) == 2:
        prompt = sys.argv[1]

    elif len(sys.argv) == 3 and sys.argv[2] == '--verbose':
        prompt = sys.argv[1]
        verbose = True

    else:
        raise ValueError("Usage: Python script prompt(string) --flag")
    
    messages = [types.Content(role='user' , parts=[types.Part(text=prompt)]),]

    response = client.models.generate_content(
            model='gemini-2.5-flash',contents = messages,
            config=types.GenerateContentConfig(tools=[available_functions],
                system_instruction=system_prompt))

    if response.function_calls:
        # if LLM wants to call a function iterate over the calls
        for function_call_part in response.function_calls:
            #Print the function call details
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")

    else:
        #if the LLM just return text no function call
        print(response.text)

    usage = response.usage_metadata
    prompt_tokens = usage.prompt_token_count
    Response_tokens = usage.candidates_token_count

    if verbose:
        print(f'User prompt: {prompt}')
        print(f'Prompt tokens: {prompt_tokens}')
        print(f'Response tokens: {Response_tokens}')
       


if __name__ == "__main__":
    main()
