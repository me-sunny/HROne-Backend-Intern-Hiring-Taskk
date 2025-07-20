from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None

mongodb = MongoDB()

async def connect_to_mongo(uri: str):
    mongodb.client = AsyncIOMotorClient(uri)

async def close_mongo_connection():
    if mongodb.client:
        mongodb.client.close()
