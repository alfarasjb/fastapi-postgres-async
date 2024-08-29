import secrets
from typing import Any
import datetime
import jwt
from fastapi import HTTPException
import bcrypt
JWT_SECRET = secrets.token_hex(16)
JWT_ALGORITHM = "HS256"
EXPIRE_MINUTES = 30


def sign(email: str) -> str:
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=EXPIRE_MINUTES)
    payload = {
        "sub": email,
        "exp": expire
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode(token: str) -> Any:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Token")


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
