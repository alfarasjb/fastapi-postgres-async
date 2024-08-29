import secrets
from typing import Any

import jwt
from fastapi import HTTPException

JWT_SECRET = secrets.token_hex(16)
JWT_ALGORITHM = "HS256"


def sign(email: str) -> str:
    payload = {
        "email": email
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode(token: str) -> Any:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Token")