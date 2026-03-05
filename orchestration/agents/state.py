from enum import Enum
from datetime import datetime
from typing import Optional, List, get_type_hints
from dataclasses import fields, dataclass, field
from pydantic import create_model, BaseModel


class ExperienceLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class UserProfile(BaseExceptionGroup):
    email: str
    certifications: list[str]
    applied_skills: list[str]


class Days(Enum):
    sunday = "sunday"
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    saturday = "saturday"


class StudentInput(BaseModel):
    topics: List[str]
    certification: Optional[str] = None
    availability_hours_per_week: Optional[int] = None
    preferred_study_days: Optional[List[Days]] = None
    timezone: Optional[str] = None
    experience_level: Optional[ExperienceLevel] = ExperienceLevel.BEGINNER


class LearningPath(BaseModel):
    title: str
    url: str
    level: Optional[ExperienceLevel]
    estimated_duration_hours: Optional[float]
    related_certification: Optional[str]


class StudySession(BaseModel):
    title: str
    duration_hours: float
    milestone: str
    url: str
    date: datetime


class StudyPlan(BaseModel):
    total_hours: float
    target_exam: Optional[str]
    sessions: List[StudySession]


class EngagementPlan(BaseModel):
    hours_per_day: int
    days_per_week: list[Days]


class Status(Enum):
    APPROVED = "approved"
    MODIFY = "approved"
    PENDING = "pending"


class ReadinessStatus(BaseModel):
    status: Status = field(default_factory=Status)
    feedback: Optional[str] = None
class WorkflowMetadata(BaseModel):
    state_version: int
    last_updated_by: str
    timestamp: datetime


class WorkflowState(BaseModel):
    user_input: StudentInput
    metadata: WorkflowMetadata
    target_exam: str
    generated_study_plan: StudyPlan
    readiness: Optional[ReadinessStatus] = field(default_factory=ReadinessStatus)


class StudentReadinessCheck(BaseModel):
    prompt: str
    current_state: WorkflowState
