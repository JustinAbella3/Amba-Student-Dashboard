import sys
from pathlib import Path

# Add the Backend directory to Python path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(backend_dir))

from configurations import client

def clear_database():
    db = client["Amba"]
    
    # Clear all collections
    db.assignment_completions.delete_many({})
    db.student_daily_stats.delete_many({})
    db.daily_overall_stats.delete_many({})
    
    # Verify collections are empty
    assignments = db.assignment_completions.count_documents({})
    student_stats = db.student_daily_stats.count_documents({})
    overall_stats = db.daily_overall_stats.count_documents({})
    
    print(f"Cleared database:")
    print(f"- Assignments: {assignments} documents")
    print(f"- Student Stats: {student_stats} documents")
    print(f"- Overall Stats: {overall_stats} documents")

if __name__ == "__main__":
    clear_database() 