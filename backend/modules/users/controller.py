from datetime import timedelta
from fastapi import Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from database import get_db
from modules.users.models import (
    UserCreate, authenticate_user, create_access_token,
    create_user, get_user_by_username, verify_token
)

class UsersController:

    @staticmethod
    def register(username: str, password: str, db: Session):
        db_user = get_user_by_username(db, username=username)
        if db_user:
            raise HTTPException(status_code=400, detail="User already registered")
        return create_user(db=db, user=UserCreate(username=username, password=password))

    @staticmethod
    def login_for_access_token(form_data: OAuth2PasswordRequestForm, db: Session):
        user = authenticate_user(form_data.username, form_data.password, db)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        access_token = create_access_token(
            data={"sub": user.username}, expire_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    def verify_token(token: str):
        verify_token(token=token)
        return {"message": "Token is valid"}
