from typing import Optional

from pydantic import Field, PostgresDsn, model_validator
from pydantic_settings import BaseSettings


# Do this instead of credentials
class Settings(BaseSettings):
    POSTGRES_USER: str = Field("postgres", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field("postgres", env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field("async_db", env="POSTGRES_DB")
    POSTGRES_HOST: str = Field("localhost", env="POSTGRES_HOST")
    POSTGRES_PORT: str = Field("5433", env="POSTGRES_PORT")
    ASYNC_POSTGRES_URI: Optional[PostgresDsn] = None
    TEST_POSTGRES_URI: Optional[PostgresDsn] = None

    class Config:
        # Used to configure the behavior of the Pydantic Model.
        case_sensitive = True
        env_file = ".env"
        # This will ignore extra fields in .env, that are not defined in the model
        # Other Options: "allow" or "forbid" (default)
        extra = "ignore"

    @model_validator(mode='after')
    def assemble_db_connection(cls, model) -> Optional[PostgresDsn]:
        if model.ASYNC_POSTGRES_URI:
            return model.ASYNC_POSTGRES_URI

        uri = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=model.POSTGRES_USER,
            password=model.POSTGRES_PASSWORD,
            host=model.POSTGRES_HOST,
            port=int(model.POSTGRES_PORT),
            path=model.POSTGRES_DB
        )
        model.ASYNC_POSTGRES_URI = str(uri)  # Set this as attribute
        model.TEST_POSTGRES_URI = model.ASYNC_POSTGRES_URI.replace(model.POSTGRES_DB, 'test_db')
        return uri

