import os
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()
MONGO_DETAILS=os.getenv("MONGO_URI")

class Database:
    client: AsyncIOMotorClient = None
    db: None

db = Database()

async def connect_to_mongo():
    print("Connecting to MongoDB...")
    db.client = AsyncIOMotorClient(MONGO_DETAILS, tlsAllowInvalidCertificates=True, tlsAllowInvalidHostnames=True)
    try:
        await db.client.admin.command('ismaster')
        db.db = db.client.get_database("resource_monitoring_db")
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        raise

async def close_mongo_connection():
    print("Closing MongoDB connection...")
    if db.client:
        db.client.close()
        print("MongoDB connection closed.")