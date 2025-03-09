from datetime import datetime
from typing import Optional, List, Dict
from .models import (
    AssignmentCompletion, 
    StudentDailyStats, 
    DailyOverallStats, 
    StudentPerformanceSummary
)

def compute_points(row: Dict) -> Dict:
    """Compute mastery and perseverance points for a single assignment"""
    try:
        points_possible = float(row.get("Points Possible", 0)) or 0
        score_best = float(row.get("Score Best Ever", 0)) or 0
        number_of_attempts = float(row.get("Number Of Attempts", 0)) or 0
    except (ValueError, TypeError):
        points_possible = score_best = number_of_attempts = 0

    assignment_type = row.get("Assignment Type", "")
    mastery = 0
    
    if assignment_type == "Course Challenge":
        mastery = 1 if points_possible > 0 and (score_best / points_possible) >= 0.9 else 0
    else:
        mastery = 1 if points_possible > 0 and score_best >= points_possible else 0

    return {
        "mastery_achieved": bool(mastery),
        "perseverance_points": number_of_attempts
    }

def process_daily_data(csv_data: List[Dict], export_date: datetime):
    """Process CSV data and return structured data for database insertion"""
    student_stats = {}
    assignments = []
    
    for row in csv_data:
        # Debug each row's assignment name
        assignment_name = row.get("Assignment Name", "").strip()
        student_name = row.get("Student Name", "").strip()
        assignment_type = row.get("Assignment Type", "").strip()
        
        if not student_name:
            continue
            
        # Create assignment completion record regardless of type
        try:
            # Get numeric values, defaulting to 0 if empty or invalid
            points_possible = float(row.get("Points Possible", 0) or 0)
            score_best = float(row.get("Score Best Ever", 0) or 0)
            attempts = int(row.get("Number Of Attempts", 0) or 0)
            
            # Calculate points only for exercises and challenges
            points = compute_points(row) if assignment_type not in ["Video", "Article"] else {
                "mastery_achieved": False,
                "perseverance_points": 0
            }
            
            assignment = AssignmentCompletion(
                export_date=export_date,
                student_name=student_name,
                assignment_name=assignment_name,
                assignment_type=assignment_type,
                points_possible=points_possible,
                score_best=score_best,
                number_of_attempts=attempts,
                mastery_achieved=points["mastery_achieved"],
                perseverance_points=points["perseverance_points"]
            )
            assignments.append(assignment)
            
            # Only update stats for exercises and challenges
            if assignment_type not in ["Video", "Article"]:
                if student_name not in student_stats:
                    student_stats[student_name] = {
                        "mastery_points": 0,
                        "perseverance_points": 0,
                        "course_challenges": 0
                    }
                
                stats = student_stats[student_name]
                stats["mastery_points"] += points["mastery_achieved"]
                stats["perseverance_points"] += points["perseverance_points"]
                if assignment_type == "Course Challenge" and points["mastery_achieved"]:
                    stats["course_challenges"] += 1
                    
        except Exception as e:
            print(f"Error processing row: {row}")
            print(f"Error details: {str(e)}")
            continue
    
    return assignments, student_stats

