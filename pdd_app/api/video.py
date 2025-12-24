from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from pdd_app.db.models import Video, Comment, User
from pdd_app.db.schema import VideoSchema, CommentSchema
from pdd_app.db.database import get_db

video_router = APIRouter(prefix="/videos", tags=["Videos"])


@video_router.get("/", response_model=List[VideoSchema])
def list_videos(db: Session = Depends(get_db)):
    videos = db.query(Video).all()
    return videos


@video_router.get("/{video_id}", response_model=VideoSchema)
def video_detail(video_id: int, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


@video_router.post("/{video_id}/comment", response_model=dict)
def add_comment(video_id: int, comment: CommentSchema, user_id: int = 1, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    new_comment = Comment(
        video_id=video_id,
        user_id=user_id,
        text=comment.text,
        created_at=datetime.utcnow()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return {"message": "Comment added"}


@video_router.post("/{video_id}/like", response_model=dict)
def like_video(video_id: int, user_id: int = 1, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    video.likes_count = video.likes_count + 1 if video.likes_count else 1
    db.add(video)
    db.commit()
    db.refresh(video)
    return {"message": "Video liked", "total_likes": video.likes_count}
