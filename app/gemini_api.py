from typing import Union

from fastapi import FastAPI
import os
from dotenv import load_dotenv
import PIL.Image

 
app = FastAPI()

import pathlib
import textwrap
import requests

import google.generativeai as genai



load_dotenv()

from IPython.display import Markdown


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

def vision (prompt,img_url):

    img = PIL.Image.open(requests.get(img_url,stream=True).raw)
    img
    model = genai.GenerativeModel('gemini-pro-vision')

    response = model.generate_content(prompt,img)

    to_markdown(response.text)

    return response.text