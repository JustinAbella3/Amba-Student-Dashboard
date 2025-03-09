import csv
from datetime import datetime
import pymongo
from pathlib import Path
import sys
import os
from os.path import dirname, abspath
from dotenv import load_dotenv

# Add the Backend directory to Python path
sys.path.append(dirname(dirname(abspath(__file__))))

from database.models import AssignmentCompletion, StudentDailyStats, DailyOverallStats
from database.schemas import compute_points, process_daily_data

def parse_date_from_filename(filename):
    filename_str = filename.name
    date_str = filename_str.split("Downloaded ")[1].split(" -")[0]
    return datetime.strptime(date_str, "%Y.%m.%d")

def insert_to_mongodb(csv_data, export_date):
    # Load environment variables
    load_dotenv()
    
    # Get MongoDB URI from environment variable
    uri = os.getenv("MONGODB_URI")
    
    if not uri:
        print("Error: MONGODB_URI environment variable not set")
        return
        
    client = pymongo.MongoClient(uri)
    db = client["Amba"]
    
    try:
        # Check if data for this date already exists
        existing_data = db.daily_overall_stats.find_one({"export_date": export_date})
        if existing_data:
            print(f"Data for {export_date.date()} already exists. Skipping...")
            return
            
        # Process the CSV data using the schema functions
        assignments, student_stats = process_daily_data(csv_data, export_date)
        
        # Debug: Print sample of assignments to be inserted
        if assignments:
            print("\nSample assignments to be inserted:")
            for a in assignments[:3]:  # Show first 3 assignments
                print(f"- {a.assignment_name} ({a.assignment_type}) for {a.student_name}")
        
        # Clear any existing data for this date
        db.assignment_completions.delete_many({"export_date": export_date})
        db.student_daily_stats.delete_many({"export_date": export_date})
        db.daily_overall_stats.delete_many({"export_date": export_date})
        
        # Insert new data and verify
        if assignments:
            result = db.assignment_completions.insert_many([a.model_dump() for a in assignments])
            print(f"\nInserted {len(assignments)} assignment records")
            
            # Verify insertion
            sample = db.assignment_completions.find_one({"_id": result.inserted_ids[0]})
            print(f"\nVerification - First inserted record:")
            print(f"- Assignment: {sample.get('assignment_name')}")
            print(f"- Type: {sample.get('assignment_type')}")
            print(f"- Student: {sample.get('student_name')}")
        
        # Calculate and insert daily stats
        daily_stats = []
        total_mastery = 0
        total_perseverance = 0
        
        for student, stats in student_stats.items():
            # Get previous totals for student
            prev_stats = db.student_daily_stats.find_one(
                {"student_name": student},
                sort=[("export_date", -1)]
            )
            
            new_stats = StudentDailyStats(
                export_date=export_date,
                student_name=student,
                daily_mastery_points=stats["mastery_points"],
                daily_perseverance_points=stats["perseverance_points"],
                total_mastery_points=(prev_stats["total_mastery_points"] if prev_stats else 0) + stats["mastery_points"],
                total_perseverance_points=(prev_stats["total_perseverance_points"] if prev_stats else 0) + stats["perseverance_points"],
                course_challenges_passed=stats["course_challenges"],
                rank_by_mastery=0,
                rank_by_perseverance=0
            )
            daily_stats.append(new_stats)
            total_mastery += stats["mastery_points"]
            total_perseverance += stats["perseverance_points"]
        
        # Calculate rankings
        sorted_by_mastery = sorted(daily_stats, key=lambda x: x.total_mastery_points, reverse=True)
        sorted_by_perseverance = sorted(daily_stats, key=lambda x: x.total_perseverance_points, reverse=True)
        
        for i, stats in enumerate(sorted_by_mastery, 1):
            stats.rank_by_mastery = i
        for i, stats in enumerate(sorted_by_perseverance, 1):
            stats.rank_by_perseverance = i
        
        # Insert daily student stats
        if daily_stats:
            db.student_daily_stats.insert_many([s.model_dump() for s in daily_stats])
            print(f"Inserted {len(daily_stats)} student daily stats")
        
        # Insert overall daily stats
        overall_stats = DailyOverallStats(
            export_date=export_date,
            total_mastery_points=total_mastery,
            total_perseverance_points=total_perseverance,
            total_course_challenges_passed=sum(s["course_challenges"] for s in student_stats.values()),
            average_mastery_points=total_mastery / len(student_stats) if student_stats else 0,
            average_perseverance_points=total_perseverance / len(student_stats) if student_stats else 0
        )
        db.daily_overall_stats.insert_one(overall_stats.model_dump())
        print("Inserted daily overall stats")
    except Exception as e:
        print(f"Error processing CSV: {str(e)}")

def main():
    # Get path to CSV files
    csv_dir = Path(dirname(dirname(abspath(__file__)))) / "documents" / "khan_csv_files"
    files = list(csv_dir.glob("*.csv"))
    
    if not files:
        print("No CSV files found in the khan_csv_files directory")
        return
    
    for file in files:
        print(f"\nProcessing {file.name}...")
        try:
            # Read CSV file with explicit encoding and handle any BOM
            with open(file, 'r', encoding='utf-8-sig') as csvfile:
                # Read as CSV first
                reader = csv.DictReader(csvfile)
                
                # Verify column names
                print("\nCSV headers:", reader.fieldnames)
                
                # Convert to list and verify first row
                data = list(reader)
                if data:
                    print("\nFirst row raw data:")
                    for key, value in data[0].items():
                        print(f"{key}: '{value}'")
                
                print(f"\nRead {len(data)} rows from CSV")
            
            # Get date from filename and process
            export_date = parse_date_from_filename(file)
            insert_to_mongodb(data, export_date)
            print(f"Successfully processed {file.name}")
        except Exception as e:
            print(f"Error processing {file.name}: {str(e)}")

if __name__ == "__main__":
    main()
