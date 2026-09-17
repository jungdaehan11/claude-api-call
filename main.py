from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

buggy_code = """
def add(a, b):
    return a - b
"""

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=f"Review this code:\n{buggy_code}",
    config=types.GenerateContentConfig(
        system_instruction="You are a terse senior code reviewer. Give feedback in one paragraph.",
        max_output_tokens=2048,
    ),
)

print(response.text)