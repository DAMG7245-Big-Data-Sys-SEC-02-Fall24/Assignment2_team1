from fastapi import APIRouter, Depends, Form, HTTPException, Body
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Dict
from app.services.database_service import get_db
from app.services.auth_service import verify_token  # Assuming token validation is handled in auth_service
import logging

# Initialize the router for document routes
router = APIRouter()

# Define OAuth2 scheme for JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Configure logging
logging.basicConfig(level=logging.INFO)


# Route to query document based on a user-provided query
@router.post("/documents/query", tags=["Query"])
async def query_endpoint(
        query: Dict[str, str] = Body(...),
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    """
    Endpoint to query a document based on user input.
    """
    try:
        # Verify the JWT token and get user email
        user_email = verify_token(token)
        if not user_email:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        # Extract query parameters from the body
        document_name = query.get("document_name")
        query_text = query.get("query_text")
        model_type = query.get("model_type")
        gpt_model = query.get("gpt_model")

        if not document_name or not query_text or not model_type or not gpt_model:
            raise HTTPException(status_code=400, detail="Missing required parameters in request body")

        # Here, implement actual querying logic
        logging.info(f"User {user_email} is querying document '{document_name}' with query: {query_text}")

        # For demonstration purposes, a mock response is returned
        response = f"Query successful for document '{document_name}' with query '{query_text}'."
        return {"response": response}

    except Exception as e:
        logging.error(f"An error occurred during the query process: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred while querying the document: {str(e)}")


# Route to summarize a document based on user input
@router.post("/documents/summarize", tags=["Summary"])
async def summarize_endpoint(
        summary_request: Dict[str, str] = Body(...),
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    """
    Endpoint to summarize a document.
    """
    try:
        # Verify the JWT token and get user email
        user_email = verify_token(token)
        if not user_email:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        # Extract summary parameters from the body
        document_name = summary_request.get("document_name")
        model_type = summary_request.get("model_type")
        gpt_model = summary_request.get("gpt_model")
        if not document_name or not model_type or not gpt_model:
            raise HTTPException(status_code=400, detail="Missing required parameters in request body")

        # Here, implement actual summarization logic
        logging.info(f"User {user_email} is summarizing document '{document_name}' using model '{gpt_model}'")

        # For demonstration purposes, a mock response is returned
        response = f"Summary successful for document '{document_name}'."
        return {"summary": response}

    except Exception as e:
        logging.error(f"An error occurred during the summarization process: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred while summarizing the document: {str(e)}")