from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List
from app.services.database_service import get_db
from app.services.auth_service import verify_token # Assuming token validation is handled in auth_service

# Initialize the router for authentication routes
router = APIRouter()

# Define OAuth2 scheme for JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.get("/query",tags=["Query"])
async def summary(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Verify the JWT token and get user information
    user_email = verify_token(token)
    if not user_email:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"message": f"You have access to this protected Querying Route, {user_email}"}

@router.post("/query", tags=["Query"])
async def query_endpoint(query: dict, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_email = verify_token(token)
    if not user_email:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user_query = query.get('query')
    # Process the query here
    return {"result": f"You have access to this protected Querying Route, {user_email}\nQuery received: {user_query}"}