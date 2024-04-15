from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, crud
import uvicorn
import pathlib
import textwrap
import google.generativeai as genai
import IPython.display
from IPython.display import Markdown
import os
from dotenv import load_dotenv
import PIL.Image
import textwrap
import requests
import logging
from typing import Union


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

user_credits = {}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def to_markdown(text):
    text = text.replace('•', '*')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
load_dotenv()
GOOGLE_API_KEY = ('AIzaSyBBb3rHORq9M0MP-JUk5vsw7JFgfDVmsto')

genai.configure(api_key=GOOGLE_API_KEY)

def vision(prompt: str, img_url: str) -> Union[str, Markdown]:
    try:
        img_response = requests.get(img_url, stream=True)
        img_response.raise_for_status()  # Ensure the image request was successful
        img = PIL.Image.open(requests.get(img_url, stream=True).content)

        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content(prompt)
        return to_markdown(response.text)

    except requests.exceptions.RequestException as e:
        logging.exception(f"Error downloading image: {e}")
        return "Error downloading image. Please check the URL."

    except Exception as e:
        logging.exception("Error in vision function:")
        return "Error processing image. Please try again later."


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/signup/")
async def signup(request: Request, username: str = Form(...), password: str = Form(...)):
    global user_credits

    if username in user_credits:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Assign credits to the user (in memory)
    user_credits[username] = 3  # Assign 3 credits to the new user

    # Render signup success template with username and assigned credits
    return templates.TemplateResponse("signup_success.html", {"request": request, "username": username, "credits": user_credits[username]})


@app.get("/signup/", response_class=HTMLResponse)
async def show_signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/login/")
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(username, db)
    if not db_user or db_user.password != password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return templates.TemplateResponse("signup_success.html", {"request": request, "username": username})

@app.get("/login/", response_class=HTMLResponse)
async def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/api/gemini")
def gemini(prompt, img_url):
    return vision(prompt, img_url)



