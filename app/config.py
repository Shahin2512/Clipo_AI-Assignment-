from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    MONGO_URL = os.getenv("MONGO_URL")
    DB_NAME = os.getenv("DB_NAME")
    REDIS_BROKER = os.getenv("REDIS_BROKER")

settings = Settings()
