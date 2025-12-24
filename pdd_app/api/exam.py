from fastapi import HTTPException, Depends, APIRouter
from pdd_app.db.models import Exam
from pdd_app.db.schema import ExamSchema, ExamCreateSchema
from pdd_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

exam_router = APIRouter(prefix='/exam', tags=['Exam'])


@exam_router.post('/', response_model=ExamSchema)
async def exam_create(
    exam: ExamCreateSchema,
    db: Session = Depends(get_db)
):
    exam_db = Exam(**exam.dict())
    db.add(exam_db)
    db.commit()
    db.refresh(exam_db)
    return exam_db


@exam_router.get('/', response_model=List[ExamSchema])
async def exam_list(db: Session = Depends(get_db)):
    return db.query(Exam).all()


@exam_router.get('/exam/{exam_id}/', response_model=ExamSchema)
async def product_detail(exam_id: int, db: Session = Depends(get_db)):
    exam_db = db.query(Exam).filter(Exam.id == exam_id).first()
    if exam_db is None:
        raise HTTPException(status_code=401, detail='Андай маалымат жок')
    return exam_db


@exam_router.put('/{exam_id}/', response_model=ExamSchema)
async def exam_update(exam_id: int, exam: ExamSchema, db: Session = Depends(get_db)):
    exam_db = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam_db:
        raise HTTPException(status_code=401, detail='Андай маалымат жок')

    for product_key, product_value in exam.dict().items():
        setattr(exam_db, product_key, product_value)
    db.add(exam_db)
    db.commit()
    db.refresh(exam_db)
    return exam_db


@exam_router.delete('/{exam_id}/', response_model=dict)
async def exam_delete(exam_id: int, db: Session = Depends(get_db)):
    exam_db = db.query(Exam).filter(Exam.id == exam_id).first()
    if exam_db is None:
        raise HTTPException(status_code=401, detail='Андай маалымат жок')
    db.delete(exam_db)
    db.commit()
    return {'message': 'Deleted'}

