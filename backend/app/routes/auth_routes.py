from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.app.controllers.auth_controller import register_user, login_user, get_all_users
from backend.app.models.user_model import UserRegisterModel, UserLoginModel, UserListResponse
from backend.app.services.database_service import get_db

router = APIRouter()

@router.post("/register")
def register(user: UserRegisterModel, db: Session = Depends(get_db)):
    return register_user(user, db)

@router.post("/login")
def login(user: UserLoginModel, db: Session = Depends(get_db)):
    return login_user(user, db)

@router.get("/users", response_model=List[UserListResponse])
def read_users(db: Session = Depends(get_db)):
    return get_all_users(db)