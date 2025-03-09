import pymongo
import os

# Try to import dotenv, but handle the case where it's not installed
try:
    from dotenv import load_dotenv
    # Load environment variables
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed. Install with: pip install python-dotenv")
    # Continue without dotenv

def create_indexes():
    # Get MongoDB URI from environment variable
    uri = os.getenv("MONGODB_URI")
    
    if not uri:
        print("Error: MONGODB_URI environment variable not set")
        return
        
    client = pymongo.MongoClient(uri)
    db = client["Amba"]
    
    # Create indexes for assignment_completions
    db.assignment_completions.create_index([("student_name", 1), ("export_date", -1)])
    
    # Create indexes for student_daily_stats
    db.student_daily_stats.create_index([("student_name", 1), ("export_date", -1)])
    
    # Create index for daily_overall_stats
    db.daily_overall_stats.create_index([("export_date", -1)])
    
    print("Indexes created successfully")

if __name__ == "__main__":
    create_indexes() 