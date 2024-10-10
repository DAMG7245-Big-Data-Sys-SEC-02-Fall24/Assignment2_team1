from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from app.controllers.auth_controller import register_user, login_user, get_all_users
from app.models.user_model import UserRegisterModel, UserLoginModel, UserListResponse
from app.services.database_service import get_db
from app.services.auth_service import get_current_user  # Assuming token validation is handled in auth_service

# Initialize the router for authentication routes
router = APIRouter()

# Define OAuth2 scheme for JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Route for user registration (not protected)
@router.post("/register", tags=["Authentication"])
def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str =Form(...),
    db: Session = Depends(get_db)):
    register_data=UserRegisterModel(Username=username,Email=email,Password=password)
    return register_user(register_data, db)

# Route for user login
@router.post("/login", tags=["Authentication"])
def login(
    email: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    login_data = UserLoginModel(Email=email, Password=password)
    return login_user(login_data, db)

# Route to fetch all registered users (protected)
@router.get("/users", response_model=List[UserListResponse], tags=["Authentication"])
def read_users(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return get_all_users(db)

# Logout endpoint
@router.post("/logout", tags=["Authentication"])
def logout(current_user: str = Depends(get_current_user)):
    # If you have token invalidation logic, implement it here.
    # For stateless JWT tokens, you might not need to do anything.
    return {"message": "Successfully logged out."}
