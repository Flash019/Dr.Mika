# STEP1: SETUP GROQ API KEY
# STEP2: CONVERT IMAGE TO REQUIRED FORMAT 
# STEP3: SETUP MULTIMODEL LLM 

import os 
from dotenv import load_dotenv
load_dotenv()

GROQ_KEY = os.getenv("GROQ_API_KEY")

from groq import Groq
import base64 # Convert Bits/bites ---> Strings | Use for encoding and decoding 
import mimetypes 
client=Groq(api_key=GROQ_KEY)

mimetypes.add_type("image/webp", ".webp") # mimetypes doesnot include .webp as default so we need to set it manually 

image_path = "testt.webp"

 # Detect MIME type

mime_type, _ = mimetypes.guess_type(image_path)
if not mime_type:
    raise ValueError(f"Cannot detect file type for: {image_path}")  # can be .png, .jpg, .jpeg, .webp, .pdf, .docx etc.

# File open 
with open(image_path, "rb") as image_file: #rb ---> read binary
    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

query = "Is there something wrong with my face ? "
model="meta-llama/llama-4-maverick-17b-128e-instruct"
messages = [
    {
        "role":"user",
        "content": [
            {
                "type": "text",
                "text": query
            },
            {
                "type": "image_url",
            "image_url":  {
                "url":  f"data:{mime_type};base64,{encoded_image}"
                },
            },
        ],
    }
]

# API Calls 
chat_completion = client.chat.completions.create(
    messages=messages,
    model=model
)
print(chat_completion.choices[0].message.content)