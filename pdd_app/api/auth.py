from datetime import timedelta, datetime
from fastapi import HTTPException, Depends, APIRouter
from pdd_app.db.models import User, Refresh
from pdd_app.db.schema import UserSchema, UserProfileLoginSchema
from pdd_app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import Optional
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from pdd_app.config import (ALGORITHM, SECRET_KEY,
                               ACCESS_TOKEN_LIFETIME,
                               REFRESH_TOKEN_LIFETIME)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
auth_router = APIRouter(prefix='/auth', tags=['Auth'])


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta]  = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_LIFETIME))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_LIFETIME))


@auth_router.post('/register', response_model=dict)
async def register(user: UserSchema, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.username == user.username).first()
    email_db = db.query(User).filter(User.email == user.email).first()

    if user_db:
        raise HTTPException(status_code=400, detail='username бар экен')

    if email_db:
        raise HTTPException(status_code=400, detail='email бар экен')

    hash_password = get_password_hash(user.password)

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        age=user.age,
        password=hash_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Registered"}


@auth_router.post('/login')
async def login(form_data: UserProfileLoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail='Маалымат туура эмес')
    access_token = create_access_token({"sub": user.username})
    refresh_token = create_refresh_token({"sub": user.username})

    new_token = Refresh(user_id = user.id, token = refresh_token)
    db.add(new_token)
    db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type":"bearer"}


@auth_router.post('/logout', response_model=dict)
async def logout(refresh_token: str,db: Session = Depends(get_db)):
    stored_token = db.query(Refresh).filter(Refresh.token == refresh_token).first()

    if not stored_token:
        raise HTTPException(status_code=401, detail='Маалымат туура эмес')

    db.delete(stored_token)
    db.commit()

    return {"message": "Вышли"}


@auth_router.post('refresh/')
async def refresh(refresh_token: str,db: Session = Depends(get_db)):
    stored_token = db.query(Refresh).filter(Refresh.token == refresh_token).first()

    if not stored_token:
        raise HTTPException(status_code=401, detail='Маалымат туура эмес')

    access_token = create_access_token({"sub": stored_token.id})

    return {"access_token": access_token,"token_type":"bearer"}

