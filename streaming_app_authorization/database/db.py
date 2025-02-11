from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

'''Подключение к MongoDB асинхронное'''
async_client = AsyncIOMotorClient(os.getenv('MONGODB_URL'))
async_db = async_client[os.getenv('MONGODB_DB_NAME')]
async_collection = async_db[os.getenv('MONGODB_COLLECTION_NAME')]

'''Подключение к MongoDB синхронное'''
# sync_client = MongoClient(os.getenv('MONGODB_URL'))
# sync_db = sync_client[os.getenv('MONGODB_DB_NAME')]
# sync_collection = sync_db[os.getenv('MONGODB_COLLECTION_NAME')]
