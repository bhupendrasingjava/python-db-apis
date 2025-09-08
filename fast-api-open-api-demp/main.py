from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client with API key from .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize FastAPI app
app = FastAPI()

# Request schema
class PromptRequest(BaseModel):
    prompt: str

@app.get("/ping")
def ping():
    return {"status": "ok", "message": "FastAPI is running 🚀"}

@app.post("/ask")
def ask_openai(request: PromptRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # can be changed to gpt-4o or gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": request.prompt}
            ]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}
