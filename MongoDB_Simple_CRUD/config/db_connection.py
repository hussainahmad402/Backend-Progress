from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file in the MongoDB folder
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

# Get MongoDB connection URL
DB_URL = os.getenv("DB_URL")

def get_db():
    """Establish MongoDB connection"""
    try:
        client = MongoClient(DB_URL)
        db = client["new_database"]
        print("✅ MongoDB Connection Successful!")
        return db
    except Exception as e:
        print(f"❌ MongoDB Connection Failed: {e}")
        return None  # Prevents app crashes if DB connection fails
