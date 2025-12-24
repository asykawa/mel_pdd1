from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from pdd_app.db.models import AnswerOption, Question
from pdd_app.db.database import SessionLocal
from pdd_app.db.schema import AnswerOptionCreateSchema


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


answer_router = APIRouter(prefix="/answers", tags=["AnswerOptions"])


@answer_router.get("/{question_id}", response_model=List[AnswerOptionCreateSchema])
def list_answers(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question.options


@answer_router.post("/{question_id}", response_model=AnswerOptionCreateSchema)
def create_answer(question_id: int, answer: AnswerOptionCreateSchema, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    new_answer = AnswerOption(
        text=answer.text,
        is_correct=answer.is_correct,
        question_id=question_id
    )
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer


@answer_router.put("/{answer_id}", response_model=AnswerOptionCreateSchema)
def update_answer(answer_id: int, answer: AnswerOptionCreateSchema, db: Session = Depends(get_db)):
    db_answer = db.query(AnswerOption).filter(AnswerOption.id == answer_id).first()
    if not db_answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    db_answer.text = answer.text
    db_answer.is_correct = answer.is_correct
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


@answer_router.delete("/{answer_id}")
def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    db_answer = db.query(AnswerOption).filter(AnswerOption.id == answer_id).first()
    if not db_answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    db.delete(db_answer)
    db.commit()
    return {"message": "Deleted"}
