from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "skillbytes")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

# Collections
users_col = db["users"]
exams_col = db["exams"]
subjects_col = db["subjects"]
chapters_col = db["chapters"]
questions_col = db["questions"]
quiz_sessions_col = db["quiz_sessions"]
analytics_col = db["analytics"]

async def get_db():
    return db
