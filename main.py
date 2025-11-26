import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import SYSTEM_PROMPT
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
response = client.models.generate_content(model="gemini-2.0-flash-001", 
                                          contents=messages,
                                          config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT))

# Print response, if the --verbose flag is set, print debugging information.
print(response.text)
if "--verbose" in sys.argv[1:]:
    print("User prompt: ", prompt)
    print("Prompt tokens:",response.usage_metadata.prompt_token_count)
    print("Response tokens:",response.usage_metadata.candidates_token_count)