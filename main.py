def main():
    import os
    import sys
    from dotenv import load_dotenv
    from google import genai
    from google.genai import types
    from system_prompt import system_prompt
    from functions.get_files_info import schema_get_files_info
    from functions.get_file_content import schema_get_file_content
    from functions.run_python_file import schema_run_python_file
    from functions.write_file import schema_write_file
    from functions.call_function import call_function


    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client  =genai.Client(api_key=api_key)

    available_functions = types.Tool(
            function_declarations=
            [ schema_get_files_info ,
              schema_get_file_content,
              schema_run_python_file,
              schema_write_file],)
    
    
    
    verbose = False
    if len(sys.argv) == 2:
        prompt = sys.argv[1]

    elif len(sys.argv) == 3 and sys.argv[2] == '--verbose':
        prompt = sys.argv[1]
        verbose = True

    else:
        raise ValueError("Usage: Python script prompt(string) --flag")

    #This version of implementation follows the google sdk logic
    messages = [types.Content(role='user' , parts=[types.Part(text=prompt)]),]
    Max_iterations = 20

    for i in range(Max_iterations):
        response = client.models.generate_content(
                model='gemini-3.5-flash-lite',contents = messages,
                config=types.GenerateContentConfig(tools=[available_functions],
                system_instruction=system_prompt))


        
        if response.candidates:
            # Appending the response to messages 
            for candidate in response.candidates:
                if candidate.content is not None:
                    messages.append(candidate.content)


        if not response.function_calls:
            #No more function_calls -> model gives a final answer
            print(response.text)
            break

        if response.function_calls:
            # if LLM wants to call a function iterate over the calls
            for function_call_part in response.function_calls:
                result_message = call_function(function_call_part , verbose=verbose)
                if (
                    not result_message.parts
                    or not result_message.parts[0].function_response
                    or not result_message.parts[0].function_response.response
                ):
                    raise Exception("Fatal:no response from the function call")
                if verbose:
                    print(f"-> {result_message.parts[0].function_response.response}")  

                messages.append(result_message)

                

    else:
        print("Max iterations(20) reached without a final response.")
        sys.exit(1)


    usage = response.usage_metadata
    if usage is not None:
        prompt_tokens = usage.prompt_token_count
        Response_tokens = usage.candidates_token_count

    if verbose:
        print(f'User prompt: {prompt}')
        print(f'Prompt tokens: {prompt_tokens}')
        print(f'Response tokens: {Response_tokens}')
       


if __name__ == "__main__":

    main()
