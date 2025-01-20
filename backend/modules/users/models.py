from datetime import timedelta, datetime, timezone
from typing import Type

from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from config import SECRET_KEY, ALGORITHM
from database import Base, engine

from fastapi import HTTPException, Depends

passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


User.metadata.create_all(bind=engine)


class UserCreate(BaseModel):
    username: str
    password: str


def get_user_by_username(db: Session, username: str) -> Type[User] | None:
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate):
    password = passwd_context.hash(user.password)
    db_user = User(username=user.username, password=password)
    db.add(db_user)
    db.commit()
    return "done"

def authenticate_user(username: str, password: str, db: Session):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not passwd_context.verify(password, str(user.password)):
        return False
    return user

def create_access_token(data: dict, expire_delta: timedelta | None = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=403,
                detail="Token is invalide or expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=403,
            detail="Token is invalide or expired",
            headers={"WWW-Authenticate": "Bearer"},
        )