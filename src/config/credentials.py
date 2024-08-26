import os
from dotenv import load_dotenv

load_dotenv()


class Credentials:
    @classmethod
    def database_url(cls) -> str:
        return os.getenv("DATABASE_URL")
    