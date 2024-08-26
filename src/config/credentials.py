import os
from dotenv import load_dotenv

load_dotenv()

""" 
Deprecated. Do not use this. Use pydantic_settings
"""
class Credentials:
    @classmethod
    def database_url(cls) -> str:
        return os.getenv("DATABASE_URL")
    