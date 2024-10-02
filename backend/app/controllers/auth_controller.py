from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from backend.app.models.user_model import User, UserRegisterModel, UserLoginModel, UserListResponse
from backend.app.services.auth_service import pwd_context, create_access_token
from backend.app.services.database_service import get_db
from typing import List

def register_user(user: UserRegisterModel, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.Email == user.Email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.Password)
    new_user = User(Username=user.Username, Email=user.Email, PasswordHash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User registered successfully"}

def login_user(user: UserLoginModel, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.Email == user.Email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Email not found")
    
    if not pwd_context.verify(user.Password, db_user.PasswordHash):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    access_token = create_access_token(data={"sub": db_user.Email})
    return {"access_token": access_token, "token_type": "bearer"}

def get_all_users(db: Session = Depends(get_db)) -> List[UserListResponse]:
    users = db.query(User).all()
    return [UserListResponse(UserId=user.UserId, Email=user.Email) for user in users]

