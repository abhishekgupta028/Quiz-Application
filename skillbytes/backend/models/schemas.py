from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

# User Models
class UserBase(BaseModel):
    name: str
    email: str
    avatar: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: str
    created_at: datetime
    class Config:
        from_attributes = True

# Exam Models
class ExamBase(BaseModel):
    title: str
    description: str
    icon: Optional[str] = "📚"
    color: Optional[str] = "#6366f1"

class ExamCreate(ExamBase):
    pass

class Exam(ExamBase):
    id: str
    created_at: datetime

# Subject Models
class SubjectBase(BaseModel):
    exam_id: str
    title: str
    description: str
    icon: Optional[str] = "📖"

class SubjectCreate(SubjectBase):
    pass

class Subject(SubjectBase):
    id: str
    created_at: datetime

# Chapter Models
class ChapterBase(BaseModel):
    subject_id: str
    exam_id: str
    title: str
    description: str
    order: int = 1

class ChapterCreate(ChapterBase):
    pass

class Chapter(ChapterBase):
    id: str
    created_at: datetime

# Question Models
class QuestionOption(BaseModel):
    id: str
    text: str

class QuestionBase(BaseModel):
    chapter_id: str
    subject_id: str
    exam_id: str
    text: str
    options: List[QuestionOption]
    correct_option_id: str
    explanation: Optional[str] = None
    difficulty: Optional[str] = "medium"

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: str
    created_at: datetime

# Quiz Session Models
class QuizSessionCreate(BaseModel):
    user_id: str
    exam_id: str
    subject_id: str
    chapter_id: str

class QuizAnswer(BaseModel):
    session_id: str
    question_id: str
    selected_option_id: str
    question_shown_at: datetime
    answer_submitted_at: datetime

class QuizSessionComplete(BaseModel):
    session_id: str
    completed_at: datetime

class QuizSession(BaseModel):
    id: str
    user_id: str
    exam_id: str
    subject_id: str
    chapter_id: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    status: str = "in_progress"
    answers: List[dict] = []
    score: Optional[float] = None
    total_questions: Optional[int] = None
