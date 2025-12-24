from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from pdd_app.db.database import get_db
from pdd_app.db.models import User
from pdd_app.db.schema import UserSchema, UserCreateSchema

user_router = APIRouter()


@user_router.post("/users", response_model=dict)
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.username == user.username).first()
    if user_db:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
        first_name=user.first_name,
        last_name=user.last_name,
        age=user.age
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created", "user_id": new_user.id}


@user_router.get("/users", response_model=List[UserSchema])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@user_router.get("/users/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.put("/users/{user_id}", response_model=dict)
def update_user(user_id: int, user: UserCreateSchema, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    user_db.username = user.username
    user_db.email = user.email
    user_db.password = user.password
    user_db.first_name = user.first_name
    user_db.last_name = user.last_name
    user_db.age = user.age

    db.commit()
    db.refresh(user_db)
    return {"message": "User updated"}


@user_router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted"}
