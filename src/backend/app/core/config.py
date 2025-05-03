import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Public Transit Agency"
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "ballast.proxy.rlwy.net")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT",     "58107")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "railway")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "eJrhyOmgcCTXRouaWJWDBhodHxthuWpq")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")

    @property
    def db_config(self) -> dict:
        return {
            "host": self.POSTGRES_HOST,
            "port": self.POSTGRES_PORT,
            "dbname": self.POSTGRES_DB,
            "user": self.POSTGRES_USER,
            "password": self.POSTGRES_PASSWORD,
        }

settings = Settings()
