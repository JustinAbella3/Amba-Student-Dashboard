from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime
from configurations import client
from database.models import (
    AssignmentCompletion, 
    StudentDailyStats, 
    DailyOverallStats,
    StudentPerformanceSummary
)

# Fix imports to be absolute instead of relative
from database.schemas import compute_points, process_daily_data
from pydantic import BaseModel

router = APIRouter(tags=["Khan Academy Data"])

# Response Models
class StudentName(BaseModel):
    student_name: str

class RankingResponse(BaseModel):
    student_name: str
    total_mastery_points: int
    total_perseverance_points: float
    rank_by_mastery: int
    rank_by_perseverance: int

class DailyChangeResponse(BaseModel):
    export_date: datetime
    daily_mastery_points: int

@router.get("/students", response_model=List[StudentName])
async def get_all_students():
    """Get all student names."""
    try:
        # Get distinct student names and convert ObjectId to string
        cursor = client.Amba.student_daily_stats.find(
            {},
            {"student_name": 1, "_id": 0}
        )
        
        # Get unique student names using a set
        student_names = set()
        for doc in cursor:
            student_names.add(doc["student_name"])
        
        # Convert to list of StudentName objects
        return [{"student_name": name} for name in sorted(student_names)]
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/student/{student_name}", response_model=List[AssignmentCompletion])
async def get_student_progress(student_name: str):
    """Get all assignments for a specific student."""
    try:
        documents = list(client.Amba.assignment_completions.find({"student_name": student_name}))
        if not documents:
            return []
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/assignments/{assignment_type}", response_model=List[AssignmentCompletion])
async def get_assignments_by_type(assignment_type: str):
    """Get all assignments of a specific type."""
    try:
        documents = list(client.Amba.assignment_completions.find({"assignment_type": assignment_type}))
        if not documents:
            return []
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/progress/{student_name}/date-range")
async def get_student_progress_by_date(
    student_name: str,
    start_date: datetime,
    end_date: datetime
):
    """Get student progress within a date range."""
    try:
        documents = list(client.Amba.assignment_completions.find({
            "student_name": student_name,
            "date": {
                "$gte": start_date,
                "$lte": end_date
            }
        }))
        if not documents:
            return []
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 1. Current Rankings Endpoints
@router.get("/rankings/current/mastery", response_model=List[RankingResponse])
async def get_current_mastery_rankings():
    """Get current mastery rankings for all students"""
    try:
        # Get the latest date first
        latest_date = client.Amba.student_daily_stats.find_one(
            sort=[("export_date", -1)]
        )["export_date"]
        
        # Get only the latest records for each student
        pipeline = [
            # Match only the latest date
            {"$match": {"export_date": latest_date}},
            # Sort by mastery points in descending order
            {"$sort": {"total_mastery_points": -1}},
            # Add array index as rank
            {"$group": {
                "_id": None,
                "students": {"$push": "$$ROOT"}
            }},
            {"$unwind": {"path": "$students", "includeArrayIndex": "rank"}},
            # Project final format
            {"$project": {
                "_id": 0,
                "student_name": "$students.student_name",
                "total_mastery_points": "$students.total_mastery_points",
                "total_perseverance_points": "$students.total_perseverance_points",
                "rank_by_mastery": {"$add": ["$rank", 1]},
                "rank_by_perseverance": "$students.rank_by_perseverance"
            }}
        ]
        
        documents = list(client.Amba.student_daily_stats.aggregate(pipeline))
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/rankings/current/perseverance", response_model=List[RankingResponse])
async def get_current_perseverance_rankings():
    """Get current perseverance rankings for all students"""
    try:
        # Get the latest date first
        latest_date = client.Amba.student_daily_stats.find_one(
            sort=[("export_date", -1)]
        )["export_date"]
        
        # Get only the latest records for each student
        pipeline = [
            # Match only the latest date
            {"$match": {"export_date": latest_date}},
            # Sort by perseverance points in descending order
            {"$sort": {"total_perseverance_points": -1}},
            # Add array index as rank
            {"$group": {
                "_id": None,
                "students": {"$push": "$$ROOT"}
            }},
            {"$unwind": {"path": "$students", "includeArrayIndex": "rank"}},
            # Project final format
            {"$project": {
                "_id": 0,
                "student_name": "$students.student_name",
                "total_mastery_points": "$students.total_mastery_points",
                "total_perseverance_points": "$students.total_perseverance_points",
                "rank_by_mastery": "$students.rank_by_mastery",
                "rank_by_perseverance": {"$add": ["$rank", 1]}
            }}
        ]
        
        documents = list(client.Amba.student_daily_stats.aggregate(pipeline))
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. Student Progress Over Time
@router.get("/student/{student_name}/progress")
async def get_student_progress_history(student_name: str):
    """Get a student's mastery and perseverance points over time"""
    try:
        return list(client.Amba.student_daily_stats.find(
            {"student_name": student_name}
        ).sort("export_date", 1))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. Daily Change Endpoints
@router.get("/student/{student_name}/daily-changes", response_model=List[DailyChangeResponse])
async def get_student_daily_changes(student_name: str):
    """Get daily changes in mastery points for a student"""
    try:
        documents = client.Amba.student_daily_stats.find(
            {"student_name": student_name},
            {
                "export_date": 1,
                "daily_mastery_points": 1,
                "_id": 0
            }
        ).sort("export_date", 1)
        return list(documents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. Overall Progress Endpoints
@router.get("/overall/progress", response_model=List[DailyOverallStats])
async def get_overall_progress():
    """Get overall progress stats over time"""
    try:
        cursor = client.Amba.daily_overall_stats.find(
            {},
            {'_id': 0}
        ).sort("export_date", 1)
        
        return list(cursor)
    except Exception as e:
        print(f"Error in get_overall_progress: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 5. Course Challenges Progress
@router.get("/overall/course-challenges")
async def get_course_challenges_progress():
    """Get total course challenges passed over time"""
    try:
        return list(client.Amba.daily_overall_stats.find(
            {},
            {"export_date": 1, "total_course_challenges_passed": 1}
        ).sort("export_date", 1))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 6. Date Range Analysis
@router.get("/analysis/date-range")
async def get_date_range_analysis(start_date: datetime, end_date: datetime):
    """Get analysis for a specific date range"""
    try:
        return list(client.Amba.daily_overall_stats.find({
            "export_date": {
                "$gte": start_date,
                "$lte": end_date
            }
        }).sort("export_date", 1))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test")
async def test_endpoint():
    """Test endpoint to verify API connectivity"""
    return {"status": "success", "message": "API is working"}
