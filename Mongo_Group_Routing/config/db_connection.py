from pymongo import MongoClient
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

db_url=os.getenv("DB_URL")

def get_db():
    try:
        client=MongoClient(db_url)
        db=client["new_database"]
        print("✅ MongoDB Connection Successful!")
        return db

    except Exception as e:
        print(f"❌ MongoDB Connection Failed: {e}")
        return None  # Prevents app crashes if DB connection fails