from fastapi import FastAPI
from backend.app.routes import auth_routes

app = FastAPI()

app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the User Authentication API"}