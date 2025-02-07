from uvicorn import run
from fastapi import FastAPI  # , Depends, Body
from fastapi.middleware.cors import CORSMiddleware
import os
import warnings
warnings.filterwarnings("ignore")
from pydantic import BaseModel

from agent.run_cookiedao import load_data_cookiedao
from agent.agents import AutogenChat
from agent.ui_pusher import create_chat


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
    allow_origins=["*"],
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


class HumanInput(BaseModel):
    chatId: str
    msg: str


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[AutogenChat] = []

    def get_agent(self, chat_id):
        return [
            a
            for a in self.active_connections
            if a.chat_id == chat_id
        ][0]

    async def connect(self, autogen_chat: AutogenChat):
        self.active_connections.append(autogen_chat)


manager = ConnectionManager()


@app.get("/init_chat")
async def init_chat():
    chat_id = create_chat()
    autogen_chat = AutogenChat(chat_id=chat_id)
    await manager.connect(autogen_chat)
    return {
        "chatId": autogen_chat.chat_id,
    }


@app.get("/init_agent")
async def init_agent(
    chatId: str,
):
    agent = manager.get_agent(chatId)
    await agent.start("test")
    return {}


@app.post("/conversation")
async def talk(
    input_data: HumanInput,
):
    agent = manager.get_agent(input_data.chatId)
    agent.websocket.put_nowait(input_data.msg)
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    run(app, host="0.0.0.0", port=port)
