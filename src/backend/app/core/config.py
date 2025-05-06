import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Public Transit Agency"
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "*").split(",")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    HOST: str = os.getenv("HOST")
    PORT: str = os.getenv("PORT")
    DB: str = os.getenv("DB")
    PASSWORD: str = os.getenv("PASSWORD")
    USER: str = os.getenv("USER")

    @property
    def db_config(self) -> dict:
        return {
            "host": self.HOST,
            "port": self.PORT,
            "dbname": self.DB,
            "user": self.USER,
            "password": self.PASSWORD,
        }

settings = Settings()
