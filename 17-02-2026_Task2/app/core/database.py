from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.DB_NAME]

transactions = db["transactions"]
categories = db["categories"]
audit_logs = db["audit_logs"]

async def create_indexes():
    await transactions.create_index([("date", -1)])
    await transactions.create_index([("category", 1),("date",-1)])
    await transactions.create_index([("type", 1),("date",-1)])
    await transactions.create_index([("title","text"),("description","text")])
    await categories.create_index("name",unique=True)
