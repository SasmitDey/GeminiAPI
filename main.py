from dotenv import load_dotenv
import os
from google import genai

from pydantic import BaseModel #structured output

import json #better readability for structured output

load_dotenv()

google_api_key = os.getenv("gemini_api")


client = genai.Client(
    api_key=google_api_key
)

# prompt = input("Enter prompt: ")

#plain jane response
# response = client.models.generate_content(
#     # model="gemini-2.0-flash", 
#     model = "models/gemini-2.5-flash-preview-05-20",
#     contents=prompt
# )

#############################################################################
# BaseModel class for structured output
# class Recipe(BaseModel):
#     book_title : str
#     book_lines : list[str]


#response structure for structured output

# response = client.models.generate_content(
#     model="models/gemini-2.5-flash-preview-05-20",
#     contents=[prompt],
#     config={
#         "response_mime_type": "application/json",
#         "response_schema": list[Recipe],
#     },
# )

# print(response.text)      #base json

# print(json.dumps(response,indent=4))    #easier readability


# my_recipes: list[Recipe] = response.parsed

# print(my_recipes)


############################################################################
#response in chunks. How they show responses in every other LLM
# response = client.models.generate_content_stream(
#     model="models/gemini-2.5-flash-preview-05-20",
#     contents=[prompt]
# )


# for chunk in response:
#     print(chunk.text, end="")

###########################################################################
#chat feature

chat = client.chats.create(model="models/gemini-2.5-flash-preview-05-20")
while(prompt.lower()!="exit"):
    prompt = input("Enter message: ")
    response = chat.send_message_stream(prompt)
    for chunk in response:
        # print(chunk.text,end="")
        print(f"\033[35m{chunk.text}\033[0m",end="")        #if you want colored output in terminal

    print()