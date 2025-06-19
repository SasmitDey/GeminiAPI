from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

from colorama import init, Fore, Style      #for custom colors in output
init()      #initialising colorama

from pydantic import BaseModel #structured output

import json #better readability for structured output


#i want to import text documents and have gemini summarise it

#required libraries
import pathlib
import httpx

#fluid printing for text, easier on eyes and readability
import time
import sys
delay=0.007  #change as per liking(0.03 for a nice relaxing scrolling effect, very lofi!)
def pretty_print(text, delay=delay):
    for char in text:
        # sys.stdout.write(f"\033[35m{char}\033[0m")
        sys.stdout.write(f"{Fore.MAGENTA}{char}{Style.RESET_ALL}")      #colorama formatting
        sys.stdout.flush() 
        time.sleep(delay)



load_dotenv()   #loading .env file variables



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

# prompt = ("Enter message: ")
# chat = client.chats.create(model="models/gemini-2.5-flash-preview-05-20")
# while(prompt.lower()!="exit"):
#     prompt = input("Enter message: ")
#     response = chat.send_message_stream(prompt)
#     for chunk in response:
#         # print(chunk.text,end="")
#         # print(f"\033[35m{chunk.text}\033[0m",end="")        #if you want colored output in terminal
#         pretty_print(chunk.text)
#     print()

###########################################################################
#chat feature but with imported text to summmarise and talk about

#using the entire text of white nights by dostoevsky

# prompt = "Summarise the text given. Keep it concise yet omit no details."

# chat = client.chats.create(model="models/gemini-2.5-flash-preview-05-20")
# filepath = pathlib.Path('white_nights.txt')
# filetext = filepath.read_text()


# summary_response = chat.send_message_stream(f"{prompt}{filetext}")

# for chunk in summary_response:
#     pretty_print(chunk.text)
# print()

# while(prompt.lower() != exit):
#     prompt = input("Enter message: ")
#     response = chat.send_message_stream(prompt)
#     for chunk in response:
#         # print(f"\033[35m{chunk.text}\033[0m",end="")
#         try:
#             pretty_print(chunk.text)
#         except TypeError:
#             pretty_print("")
#     print()

###########################################################################

#implement file uploading so it doesn't have to print out summaries to remember context (to do)




###########################################################################

#google searching
# chat = client.chats.create(model="models/gemini-2.5-flash-preview-05-20")

# grounding_tool = types.Tool(
#     google_search=types.GoogleSearch()
# )

# config = types.GenerateContentConfig(
#     tools=[grounding_tool]
# )

# prompt = input("Enter message: ")
# while(prompt.lower() != "exit"):
#     # response = chat.send_message_stream(prompt)
#     response = chat.send_message_stream(
#         prompt,
#         config=config
#     )
#     for chunk in response:
#         # print(f"\033[35m{chunk.text}\033[0m",end="")
#         try:
#             pretty_print(chunk.text)
#         except TypeError:
#             pretty_print("")
#     print()
#     prompt = input("Enter message: ")

###########################################################################
#google searching with url context (give url to add additional context for model)

chat = client.chats.create(model="models/gemini-2.5-flash-preview-05-20")
system_instruction = os.getenv('system_instruction')

tools = []
tools.append(types.Tool(google_search=types.GoogleSearch))
tools.append(types.Tool(url_context=types.UrlContext))
# tools.append(types.Tool(code_execution=types.ToolCodeExecution))  #turn on if code execution required
                                                                    #otherwise messes up normal outputs

config = types.GenerateContentConfig(
    tools=tools,
    system_instruction=system_instruction
)

prompt = input("Enter message: ")
while(prompt.lower() != "exit"):
    # response = chat.send_message_stream(prompt)
    response = chat.send_message_stream(
        prompt,
        config=config
    )
    for chunk in response:
        # print(f"\033[35m{chunk.text}\033[0m",end="")
        try:
            pretty_print(chunk.text)
        except TypeError:
            pretty_print("")
    print()
    prompt = input("Enter message: ")