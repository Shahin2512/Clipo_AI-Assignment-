from pymongo import MongoClient
from app.config import settings

client = MongoClient(settings.MONGO_URL)
db = client[settings.DB_NAME]
videos_collection = db["videos"]
