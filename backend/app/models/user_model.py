from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List

Base = declarative_base()

class User(Base):
    __tablename__ = "Users"
    
    UserId = Column(Integer, primary_key=True, index=True)
    Username = Column(String(255), unique=True, nullable=False)
    Email = Column(String(255), unique=True, nullable=False)
    PasswordHash = Column(String, nullable=False)
    CreatedAt = Column(TIMESTAMP, server_default=func.now())

class UserRegisterModel(BaseModel):
    Username: str = Field(..., min_length=1, max_length=255, description="Username cannot be blank")
    Email: EmailStr = Field(..., description="Email must be valid")
    Password: str = Field(..., min_length=8, description="Password cannot be blank and must have at least 8 characters")
    
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

class UserLoginModel(BaseModel):
    Email: EmailStr = Field(..., description="Email must be valid")
    Password: str = Field(..., min_length=8, description="Password cannot be blank")

class UserListResponse(BaseModel):
    UserId: int
    Email: str

    class Config:
        orm_mode = True