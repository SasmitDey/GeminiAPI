from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

google_api_key = os.getenv("gemini_api")


client = genai.Client(
    api_key=google_api_key
)

content = input("Enter prompt: ")

response = client.models.generate_content(
    # model="gemini-2.0-flash", 
    model = "models/gemini-2.5-flash-preview-05-20",
    contents=f"{content}"
)

print(response.text)