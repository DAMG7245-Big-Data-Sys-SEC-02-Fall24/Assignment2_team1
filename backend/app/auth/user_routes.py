from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, EmailStr, validator
from passlib.context import CryptContext
from app.auth.jwt_handler import create_access_token
from app.db.db import get_db
from app.db.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

# Pydantic model for user registration with email and password validation
class UserRegisterModel(BaseModel):
    Username: str = Field(..., min_length=1, max_length=255, description="Username cannot be blank")
    Email: EmailStr = Field(..., description="Email must be valid")  # EmailStr validates email format
    Password: str = Field(..., min_length=8, description="Password cannot be blank and must have at least 8 characters")

    # Password validation
    @validator("Password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one number")
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in value):
            raise ValueError("Password must contain at least one lowercase letter")
        return value

# Pydantic model for user login with email and password validation
class UserLoginModel(BaseModel):
    Email: EmailStr = Field(..., description="Email must be valid")
    Password: str = Field(..., min_length=8, description="Password cannot be blank")

@router.post("/register")
def register(user: UserRegisterModel, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.Email == user.Email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.Password)
    new_user = User(Username=user.Username, Email=user.Email, PasswordHash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: UserLoginModel, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.Email == user.Email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Email not found")
    
    if not pwd_context.verify(user.Password, db_user.PasswordHash):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    access_token = create_access_token(data={"sub": db_user.Email})
    return {"access_token": access_token, "token_type": "bearer"}
