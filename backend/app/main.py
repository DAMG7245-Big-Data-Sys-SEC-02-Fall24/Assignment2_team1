from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
from app.routes import auth_routes,summary_routes
from app.services.auth_service import verify_token
from app.services.database_service import get_db


# Initialize FastAPI app
app = FastAPI()

# Define OAuth2PasswordBearer for JWT authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Global exception handler for catching unexpected errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred.", "details": str(exc)}
    )

# Include the authentication routes from the auth_routes module
app.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])

# Include the authentication routes from the summary module
app.include_router(summary_routes.router,tags=["Summary"])



# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the User Authentication API"}

# Health check route to ensure the service is running
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Example of a protected route
@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Verify the JWT token and get user information
    user_email = verify_token(token)
    if not user_email:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"message": f"You have access to this protected route, {user_email}"}

# Custom OpenAPI schema to display protected endpoints with padlock icon
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="User Authentication API",
        version="1.0",
        description="This is a user authentication API with JWT-based protection.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if "security" in openapi_schema["paths"][path][method]:
                openapi_schema["paths"][path][method]["security"] = [{"bearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
