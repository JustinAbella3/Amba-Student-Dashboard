from configurations import client

def check_assignments():
    db = client["Amba"]
    
    # Check total number of assignments
    total = db.assignment_completions.count_documents({})
    print(f"\nTotal assignments: {total}")
    
    # Check high school physics assignments
    hs_physics = db.assignment_completions.find({"assignment_name": "High school physics"})
    print("\nHigh school physics assignments:")
    for assignment in hs_physics:
        print(f"- {assignment['student_name']} ({assignment['export_date']})")
    
    # Check unique assignment names
    unique_names = db.assignment_completions.distinct("assignment_name")
    print("\nUnique assignment names:")
    for name in unique_names:
        print(f"- {name}")
        
    # Check assignments by type
    print("\nAssignments by type:")
    pipeline = [
        {"$group": {"_id": "$assignment_type", "count": {"$sum": 1}}}
    ]
    by_type = db.assignment_completions.aggregate(pipeline)
    for result in by_type:
        print(f"- {result['_id']}: {result['count']}")

if __name__ == "__main__":
    check_assignments() 