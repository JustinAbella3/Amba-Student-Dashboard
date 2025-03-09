from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

# Try to import dotenv, but handle the case where it's not installed
try:
    from dotenv import load_dotenv
    # Load environment variables from .env file
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Install with: pip install python-dotenv")
    # Continue without dotenv

# Get MongoDB URI from environment variable
uri = os.getenv("MONGODB_URI")

# If no environment variable is set, use a default for development
if not uri:
    print("Warning: MONGODB_URI environment variable not set. Using mock data for development.")
    uri = "mongodb://localhost:27017"

# Create a simple client with minimal configuration
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"MongoDB connection error: {str(e)}")
    print("Using mock data for development")

