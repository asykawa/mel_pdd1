import sys
from pathlib import Path
from fastapi import FastAPI
import uvicorn
from pdd_app.api import (
    category, auth, exam, questions, answeroptions,
    video, users, pdd_pr
)
from pdd_app.db.database import SessionLocal


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="PDD API")

app.include_router(category.category_router)
app.include_router(auth.auth_router)
app.include_router(exam.exam_router)
app.include_router(questions.question_router)
app.include_router(answeroptions.answer_router)
app.include_router(video.video_router)
app.include_router(auth.auth_router)
app.include_router(pdd_pr.model_router)


if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
