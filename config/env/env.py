from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env.development")

class Env:
    APP_NAME: str
    APP_PORT: int
    APP_VER: str

    DB_HOST: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_PORT: str
    DB_DRIVER: str

    API_KEY: str
    GROQ_LLM: str
    GROQ_API_KEY: str

    def __init__(self):
        self.APP_NAME = os.getenv("APP_NAME")
        self.APP_PORT = int(os.getenv("APP_PORT", "5000"))
        self.APP_VER = os.getenv("APP_VER", "1_3")
        self.APP_VER = self.APP_VER.replace(".", "_")


        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASS = os.getenv("DB_PASS")
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_PORT = os.getenv("DB_PORT")
        self.DB_PORT = os.getenv("DB_PORT")
        self.DB_DRIVER = os.getenv("DB_DRIVER")

        self.API_KEY = os.getenv("API_KEY")
        self.GROQ_LLM = os.getenv("GROQ_LLM")
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")