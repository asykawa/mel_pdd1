from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from pdd_app.db.models import QuestionDifficulty, ExamStatus


class UserSchema(BaseModel):
    username: str
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: int

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    email: EmailStr
    username: str
    password: str

    class Config:
        from_attributes = True


class UserProfileLoginSchema(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class CategorySchema(BaseModel):
    id: int
    category_name: str

    class Config:
        from_attributes = True


class CategoryCreateSchema(BaseModel):
    category_name: str

    class Config:
        from_attributes = True


class QuestionSchema(BaseModel):
    id: int
    text: str
    explanation: str
    category_id: int
    difficulty: QuestionDifficulty

    class Config:
        from_attributes = True


class QuestionCreateSchema(BaseModel):
    text: str
    explanation: str
    category_id: int
    difficulty: QuestionDifficulty

    class Config:
        from_attributes = True


class AnswerOptionSchema(BaseModel):
    id: int
    text: str
    question_id: int
    is_correct: Optional[bool] = False

    class Config:
        from_attributes = True


class AnswerOptionCreateSchema(BaseModel):
    text: str
    question_id: int
    is_correct: Optional[bool] = False

    class Config:
        from_attributes = True


class ExamSchema(BaseModel):
    id: int
    user_id: int
    score: int
    status: ExamStatus
    started_at: datetime
    finished_at: Optional[datetime]

    class Config:
        from_attributes = True


class ExamCreateSchema(BaseModel):
    user_id: int
    score: int
    status: ExamStatus
    started_at: datetime
    finished_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class VideoSchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    url: str
    views_count: Optional[int] = 0

    class Config:
        from_attributes = True


class VideoCreateSchema(BaseModel):
    title: str
    description: Optional[str]
    url: str

    class Config:
        from_attributes = True


class CommentSchema(BaseModel):
    id: int
    text: str
    user_id: int
    question_id: Optional[int] = None
    video_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CommentCreateSchema(BaseModel):
    text: str
    user_id: int
    question_id: Optional[int] = None
    video_id: Optional[int] = None

    class Config:
        from_attributes = True


class LikeSchema(BaseModel):
    id: int
    user_id: int
    question_id: Optional[int] = None
    video_id: Optional[int] = None
    comment_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class PddClass(BaseModel):
    id: int
    image_url: str
    predicted_label: str
    confidence: float
    created_date: datetime

    class Config:
        from_attributes = True


class LikeCreateSchema(BaseModel):
    user_id: int
    question_id: Optional[int] = None
    video_id: Optional[int] = None
    comment_id: Optional[int] = None

    class Config:
        from_attributes = True
