from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, handler):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(ObjectId(v))

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema: Any, field: Any) -> Any:
        return {"type": "string"}

class MongoBaseModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    
    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
        arbitrary_types_allowed = True

    def model_dump(self, *args, **kwargs):
        kwargs["exclude_none"] = True
        return super().model_dump(*args, **kwargs)

class OverallDailyProgress(MongoBaseModel):
    export_date: datetime
    attempted_assignments: int
    mastered_assignments: int

class StudentPerformance(MongoBaseModel):
    student_name: str
    unique_assignments: int
    total_attempts: int
    mastered_courses: int

class StudentDetailedPerformance(MongoBaseModel):
    student_name: str
    assignment_name: str
    score_at_due_date: int
    score_best_ever: int
    points_possible: int
    number_of_attempts: int
    assignment_type: str
    mastered: int

class StudentDailyProgress(MongoBaseModel):
    export_date: datetime
    student_name: str
    attempted_assignments: int
    mastered_assignments: int

class OverallProgress(MongoBaseModel):
    attempted_assignments: int
    mastered_assignments: int

class StudentDailyStats(MongoBaseModel):
    """Daily statistics for each student"""
    export_date: datetime
    student_name: str
    daily_mastery_points: int
    daily_perseverance_points: float
    total_mastery_points: int
    total_perseverance_points: float
    course_challenges_passed: int
    rank_by_mastery: int
    rank_by_perseverance: int

class AssignmentCompletion(MongoBaseModel):
    """Detailed record of each assignment completion"""
    export_date: datetime
    student_name: str
    assignment_name: str
    assignment_type: str
    points_possible: float
    score_best: float
    number_of_attempts: int
    mastery_achieved: bool
    perseverance_points: float

class DailyOverallStats(MongoBaseModel):
    """Daily aggregated statistics across all students"""
    export_date: datetime
    total_mastery_points: int
    total_perseverance_points: float
    total_course_challenges_passed: int
    average_mastery_points: float
    average_perseverance_points: float

class StudentPerformanceSummary(MongoBaseModel):
    """Current summary statistics for each student"""
    student_name: str
    total_mastery_points: int
    total_perseverance_points: float
    course_challenges_passed: int
    assignments_attempted: int
    last_updated: datetime
    current_mastery_rank: int
    current_perseverance_rank: int
