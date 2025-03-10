from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from modules.users.controller import UsersController

router = APIRouter()

# Health check route
@router.get("/health", tags=["Health check"])
async def health_check():
    return {"status": "ok"}

# User registration route
@router.post("/register", tags=["Users API"])
def register(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    return UsersController.register(username, password, db)

# User authentication route
@router.post("/token", tags=["Users API"])
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return UsersController.login_for_access_token(form_data, db)

# Token verification route
@router.get("/verify-token/{token}", tags=["Users API"])
async def verify_token_url(token: str):
    return UsersController.verify_token(token)
