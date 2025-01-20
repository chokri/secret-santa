from datetime import timedelta

from fastapi import APIRouter, Form, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from database import get_db
from modules.users.models import get_user_by_username, UserCreate, create_user, authenticate_user, create_access_token, \
    verify_token

router = APIRouter()


@router.get("/health", tags=["Health check"])
async def health_check():
    return {"status": "ok"}



@router.post("/register", tags=["Users API"])
def register( username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registred")
    return create_user(db=db, user=UserCreate(username=username, password=password))


@router.post("/token", tags=["Users API"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
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


@router.get("/verify-token/{token}", tags=["Users API"])
async def verify_token_url(token: str):
    verify_token(token=token)
    return {"message": "Token is valid"}