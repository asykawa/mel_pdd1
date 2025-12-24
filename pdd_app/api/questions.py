from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from pdd_app.db.models import Question, AnswerOption, User
from pdd_app.db.database import SessionLocal
from pdd_app.db.schema import QuestionSchema, AnswerOptionSchema


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


question_router = APIRouter(prefix="/questions", tags=["Questions"])


@question_router.get("/", response_model=List[QuestionSchema])
def list_questions(
    category: Optional[int] = Query(None),
    difficulty: Optional[str] = Query(None),
    limit: Optional[int] = Query(20),
    db: Session = Depends(get_db)
):
    query = db.query(Question)

    if category is not None:
        query = query.filter(Question.category_id == category)
    if difficulty is not None:
        query = query.filter(Question.difficulty == difficulty)

    questions = query.limit(limit).all()
    return questions


@question_router.get("/{question_id}", response_model=QuestionSchema)
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@question_router.post("/{question_id}/favorite")
def favorite_question(question_id: int, user_id: int = 1, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    return {"status": "added"}
