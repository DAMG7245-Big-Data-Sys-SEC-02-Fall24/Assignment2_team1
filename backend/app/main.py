from fastapi import FastAPI
from app.auth import user_routes

# Initialize FastAPI app
app = FastAPI()

# Register the user authentication router
app.include_router(user_routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the User Authentication API"}