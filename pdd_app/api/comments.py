from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime


from pdd_app.db.models import Comment, Like
from pdd_app.db.schema import CommentSchema, LikeSchema
from pdd_app.db.database import SessionLocal


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


comment_router = APIRouter(prefix='/comment', tags=['Comment'])


@comment_router.post('/', response_model=CommentSchema)
async def create_comment(comment: CommentSchema, db: Session = Depends(get_db)):
    comment_db = Comment(
        text=comment.text,
        user_id=comment.user_id,
        question_id=getattr(comment, 'question_id', None),
        video_id=getattr(comment, 'video_id', None)
    )
    db.add(comment_db)
    db.commit()
    db.refresh(comment_db)
    return comment_db


@comment_router.get('/', response_model=List[CommentSchema])
async def list_comments(db: Session = Depends(get_db)):
    return db.query(Comment).all()


@comment_router.get('/{comment_id}/', response_model=CommentSchema)
async def detail_comment(comment_id: int, db: Session = Depends(get_db)):
    comment_db = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment_db:
        raise HTTPException(status_code=404, detail='Комментарий не найден')
    return comment_db


@comment_router.put('/{comment_id}/', response_model=dict)
async def update_comment(comment_id: int, comment: CommentSchema, db: Session = Depends(get_db)):
    comment_db = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment_db:
        raise HTTPException(status_code=404, detail='Комментарий не найден')
    comment_db.text = comment.text
    db.add(comment_db)
    db.commit()
    db.refresh(comment_db)
    return {'message': 'Updated'}


@comment_router.delete('/{comment_id}/', response_model=dict)
async def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment_db = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment_db:
        raise HTTPException(status_code=404, detail='Комментарий не найден')
    db.delete(comment_db)
    db.commit()
    return {'message': 'Deleted'}


# ------------------- Like Router -------------------
like_router = APIRouter(prefix='/like', tags=['Like'])

@like_router.post('/', response_model=LikeSchema)
async def create_like(like: LikeSchema, db: Session = Depends(get_db)):
    like_db = Like(
        user_id=like.user_id,
        question_id=getattr(like, 'question_id', None),
        video_id=getattr(like, 'video_id', None),
        comment_id=getattr(like, 'comment_id', None)
    )
    db.add(like_db)
    db.commit()
    db.refresh(like_db)
    return like_db

@like_router.get('/', response_model=List[LikeSchema])
async def list_likes(db: Session = Depends(get_db)):
    return db.query(Like).all()

@like_router.get('/{like_id}/', response_model=LikeSchema)
async def detail_like(like_id: int, db: Session = Depends(get_db)):
    like_db = db.query(Like).filter(Like.id == like_id).first()
    if not like_db:
        raise HTTPException(status_code=404, detail='Лайк не найден')
    return like_db

@like_router.delete('/{like_id}/', response_model=dict)
async def delete_like(like_id: int, db: Session = Depends(get_db)):
    like_db = db.query(Like).filter(Like.id == like_id).first()
    if not like_db:
        raise HTTPException(status_code=404, detail='Лайк не найден')
    db.delete(like_db)
    db.commit()
    return {'message': 'Deleted'}
