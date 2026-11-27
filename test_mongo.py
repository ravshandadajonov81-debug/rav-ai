import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGO_URI")
client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("MongoDB ga muvaffaqiyatli ulandi!")
except Exception as e:
    print("Xato:", e)