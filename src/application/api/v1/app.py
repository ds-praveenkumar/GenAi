import sys
sys.path.append('src')
import os 
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
import io
from fastapi import FastAPI
import base64
from fastapi.staticfiles import StaticFiles

from agents.email_agent.gmail_agent import GmailBaseAgent

gmail_agent = GmailBaseAgent()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specific domain like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}

class ChatRequest(BaseModel):
    query: str
    
class speakRequest(BaseModel):
    text: str

@app.post("/api/v1/chat")
async def read_item( request: ChatRequest):
    """
        send query to agent 
    """
    agent_response =  gmail_agent.main( request.query )
    return {
        "response_code": 200,
        "statue": "success",
        "response": agent_response
    }
    
@app.post("/api/v1/speak")
async def speak( request: speakRequest):
    """
        send query to agent 
    """
    
    # agent_response =  gmail_agent.agent_speaker.speak( text.text )
    tts = gTTS(request.text)
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    audio_base64 = base64.b64encode(audio_fp.read()).decode("utf-8")
    return {
        "response_code": 200,
        "statue": "success",
        "audio_base64": audio_base64,
        "mime_type": "audio/mp3"
    }