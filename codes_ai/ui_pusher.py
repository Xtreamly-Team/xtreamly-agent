import firebase_admin
from datetime import datetime
from firebase_admin import credentials, firestore


cred = credentials.Certificate("./xtreamly-firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def create_chat():
    collection_ref = db.collection(f"chats")
    doc = collection_ref.add({
        "time": datetime.utcnow(),
    })

    return doc[1].id


def push_message(chat_id, agent, message):
    message = None if message is None else message.strip()
    if message is None or message == "TERMINATE" or message == "" or message == "!@#$^":
        return

    collection_ref = db.collection(f"chats/{chat_id}/messages")
    collection_ref.add({
        "chat_id": chat_id,
        "agent": agent,
        "time": datetime.utcnow(),
        "userInput": False,
        "ai": agent != "human_proxy",
        "message": message,
    })
