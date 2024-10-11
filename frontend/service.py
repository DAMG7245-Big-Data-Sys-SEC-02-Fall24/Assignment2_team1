import requests
import os
import streamlit as st

# Assuming you have your API_BASE_URL in environment variables
API_BASE_URL = os.getenv("API_BASE_URL")

def summarize_document_api(document_name, model_type, gpt_model, access_token):
    summarize_url = f"{API_BASE_URL}/documents/summarize"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.post(
            summarize_url,
            json={
                "document_name": document_name,
                "model_type": model_type,
                "gpt_model": gpt_model
            },
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("summary"), None
        else:
            return None, parse_error_response(response)
    except Exception as e:
        return None, f"An error occurred: {e}"

def query_document_api(document_name, query_text, model_type, gpt_model, access_token):
    query_url = f"{API_BASE_URL}/documents/query"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.post(
            query_url,
            json={
                "document_name": document_name,
                "query_text": query_text,
                "model_type": model_type,
                "gpt_model": gpt_model
            },
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("response"), None
        else:
            return None, parse_error_response(response)
    except Exception as e:
        return None, f"An error occurred: {e}"

def parse_error_response(response):
    try:
        error_json = response.json()
        if isinstance(error_json, dict):
            detail = error_json.get("detail")
            if isinstance(detail, list):
                # Pydantic validation errors
                messages = [f"{err['loc'][-1]}: {err['msg']}" for err in detail]
                return " ; ".join(messages)
            elif isinstance(detail, dict):
                # Custom error response
                error_message = detail.get("error", "Error")
                error_details = detail.get("details", "")
                return f"{error_message}: {error_details}"
            else:
                return detail or "An error occurred."
        else:
            return "An error occurred."
    except ValueError:
        return "An error occurred."
