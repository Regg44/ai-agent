import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import SYSTEM_PROMPT
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function
# Load local API key, you will need to input your own
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# If an empty argument is set, exit with error 1
if len(sys.argv) < 2:
    print("Sorry, please input a valid prompt")
    sys.exit(1)

# Set user prompt
prompt = sys.argv[1]

# Create a list on types.Content
messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)])
]
client = genai.Client(api_key=api_key)

# List of available functions, for now, only get_files_info
available_functions = types.Tool(
    function_declarations=[
        schema_get_file_content,
        schema_get_files_info,
        schema_run_python_file,
        schema_write_file
    ]
)
# Added the "tools" parameter to config containing the get_files_info schema.
response = client.models.generate_content(model="gemini-2.0-flash-001", 
                                          contents=messages,
                                          config=types.GenerateContentConfig(tools=[available_functions],system_instruction=SYSTEM_PROMPT))
# Print out the function calls if any
if response.function_calls != None:
    for call in response.function_calls:
        try:
            call_obj = call_function(call, verbose=("--verbose" in sys.argv[1:]))
            if call_obj.parts[0].function_response.response == None:
                raise Exception("Something went really wrong")

        except Exception as e:
            print(e)

# Print response, if the --verbose flag is set, print debugging information.
print(response.text)
if "--verbose" in sys.argv[1:]:
    print(f"-> {call_obj.parts[0].function_response.response}")
    print("User prompt: ", prompt)
    print("Prompt tokens:",response.usage_metadata.prompt_token_count)
    print("Response tokens:",response.usage_metadata.candidates_token_count)