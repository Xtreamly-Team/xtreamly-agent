from fastapi import FastAPI, BackgroundTasks, Query, UploadFile, Body, Form, Security, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

import firebase_admin
from firebase_admin import credentials, auth

auth_file_firebase = os.path.join('firebase', os.getenv('FIREBASE_SDK', 'firebase-admin.json'))
cred = credentials.Certificate(auth_file_firebase)
firebase_admin.initialize_app(cred)
security = HTTPBearer(auto_error=False)


def _current_user(token: HTTPAuthorizationCredentials = Security(security)):
    dev = os.getenv("APP_DEV", 0)
    if dev:
        return {
            'uid': 'xxx',
            'displayName': 'Pawel',
            'email': 'pawel.masior@geekforce.io',
        }
    else:
        try:
            decoded_token = auth.verify_id_token(token.credentials)
            return decoded_token
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
