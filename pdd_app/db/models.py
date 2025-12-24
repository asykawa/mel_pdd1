from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import String, Integer, Text, Boolean, DateTime, ForeignKey, Enum, Table, Column, Float
from datetime import datetime
from enum import Enum as PyEnum
from typing import List, Optional


class Base(DeclarativeBase):
    pass


class QuestionDifficulty(str, PyEnum):
    easy = "easy"
    medium = "medium"
    advanced = "advanced"


class ExamStatus(str, PyEnum):
    in_progress = "in_progress"
    passed = "passed"
    failed = "failed"
    finished = "finished"


class User(Base):
    __tablename__ = "user_profile"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    exams: Mapped[List["Exam"]] = relationship("Exam", back_populates="user")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="user")
    likes: Mapped[List["Like"]] = relationship("Like", back_populates="user")
    user_token: Mapped[List["Refresh"]] = relationship("Refresh", back_populates="user", cascade="all, delete-orphan")


class Refresh(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user_profile.id'))
    user: Mapped[User] = relationship(User, back_populates='user_token')
    token: Mapped[str] = mapped_column(String, nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __str__(self):
        return f'{self.user}'


question_exam = Table(
    "question_exam",
    Base.metadata,
    Column("question_id", ForeignKey("questions.id"), primary_key=True),
    Column("exam_id", ForeignKey("exams.id"), primary_key=True)
)


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String, unique=True)

    questions: Mapped[List["Question"]] = relationship("Question", back_populates="category")


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[QuestionDifficulty] = mapped_column(Enum(QuestionDifficulty), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    category: Mapped["Category"] = relationship("Category", back_populates="questions")
    answer_options: Mapped[List["AnswerOption"]] = relationship("AnswerOption", back_populates="question")
    exams: Mapped[List["Exam"]] = relationship("Exam", secondary=question_exam, back_populates="questions")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="question")
    likes: Mapped[List["Like"]] = relationship("Like", back_populates="question")
    pdd_classes: Mapped[List["PddClass"]] = relationship("PddClass", back_populates="question")


class AnswerOption(Base):
    __tablename__ = "answer_options"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))

    question: Mapped["Question"] = relationship("Question", back_populates="answer_options")


class Exam(Base):
    __tablename__ = "exams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id"))
    score: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[ExamStatus] = mapped_column(Enum(ExamStatus), default=ExamStatus.in_progress)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="exams")
    questions: Mapped[List["Question"]] = relationship("Question", secondary=question_exam, back_populates="exams")


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(String, nullable=False)
    views_count: Mapped[int] = mapped_column(Integer, default=0)

    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="video")
    likes: Mapped[List["Like"]] = relationship("Like", back_populates="video")


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id"))
    question_id: Mapped[Optional[int]] = mapped_column(ForeignKey("questions.id"), nullable=True)
    video_id: Mapped[Optional[int]] = mapped_column(ForeignKey("videos.id"), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="comments")
    question: Mapped[Optional["Question"]] = relationship("Question", back_populates="comments")
    video: Mapped[Optional["Video"]] = relationship("Video", back_populates="comments")
    likes: Mapped[List["Like"]] = relationship("Like", back_populates="comment")


class Like(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id"))
    question_id: Mapped[Optional[int]] = mapped_column(ForeignKey("questions.id"), nullable=True)
    video_id: Mapped[Optional[int]] = mapped_column(ForeignKey("videos.id"), nullable=True)
    comment_id: Mapped[Optional[int]] = mapped_column(ForeignKey("comments.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="likes")
    question: Mapped[Optional["Question"]] = relationship("Question", back_populates="likes")
    video: Mapped[Optional["Video"]] = relationship("Video", back_populates="likes")
    comment: Mapped[Optional["Comment"]] = relationship("Comment", back_populates="likes")


class PddClass(Base):
    __tablename__ = "pdd_classes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    image_url: Mapped[str] = mapped_column(String, nullable=True)
    predicted_label: Mapped[str] = mapped_column(String, nullable=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=True)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow(), autoincrement=True, nullable=True)
