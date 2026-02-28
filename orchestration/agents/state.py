from enum import Enum
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ExperienceLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class StudentInput(BaseModel):
    topics: List[str]
    certification_goal: Optional[str] = None
    target_exam_date: Optional[datetime] = None
    availability_hours_per_week: Optional[int] = None
    preferred_study_days: Optional[List[str]] = None
    timezone: Optional[str] = None
    experience_level: Optional[ExperienceLevel] = None



class LearningPath(BaseModel):
    title: str
    url: str
    level: Optional[str]
    estimated_duration_hours: Optional[float]
    related_certification: Optional[str]



class StudySession(BaseModel):
    week: int
    title: str
    duration_hours: float
    milestone: str



class StudyPlan(BaseModel):
    total_weeks: int
    total_hours: float
    sessions: List[StudySession]


class Status(Enum):
    APPROVED = "approved"
    MODIFY = "modify"
    CANCELLED = "cancelled"
    PENDING = "pending"


class ReadinessStatus(BaseModel):
    status: Status
    feedback: Optional[str] = None


class WorkflowMetadata(BaseModel):
    state_version: int
    last_updated_by: str
    timestamp: datetime



class WorkflowState(BaseModel):
    user_input: StudentInput
    metadata: WorkflowMetadata
    curated_learning_paths: List[LearningPath] = Field(default_factory=list)
    generated_study_plan: Optional[StudyPlan] = None
    readiness: Optional[ReadinessStatus] = None
    current_phase: Optional[str] = None
