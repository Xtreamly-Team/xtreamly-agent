from uvicorn import run
from fastapi import FastAPI, Query, Body, BackgroundTasks, HTTPException, File, UploadFile, Depends  # , Depends, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import os
import warnings
warnings.filterwarnings("ignore")
# from auth import _current_user

from run_cookiedao import load_data_cookiedao
from run_agents import _conversation

app = FastAPI(
    title="AI Cookie DAO",
    description='Agentic app.',
    version="0.0.3",
    terms_of_service="https://xtreamly.io/",
    contact={
        "name": "contact",
        "url": "https://xtreamly.io/",
    },
    license_info={
        "name": "Samlpe licence",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5000",
    "http://localhost:5001",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home(): return 'Cookie DAO hackaton'

@app.post("/load_data")
def load():  
    load_data_cookiedao()
    return "Loaded Cookie DAO data into BQ"

@app.post("/Conversation")
def talk(
    msg: str = Query("Find me most interesting agents to invest in"),
    ):  
    return _conversation(msg)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    run(app, host="0.0.0.0", port=port)
