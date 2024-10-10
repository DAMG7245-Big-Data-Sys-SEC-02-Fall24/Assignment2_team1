import streamlit as st
import requests
from utils import get_headers, API_BASE_URL, refresh_access_token

def display():
    st.title("Querying")
    st.write("This page allows you to perform queries.")

    query_text = st.text_input("Enter your query")

    if st.button("Submit Query"):
        if query_text:
            with st.spinner("Processing query..."):
                query_url = f"{API_BASE_URL}/query"
                params = {'query': query_text}
                try:
                    response = requests.get(
                        query_url,
                        headers=get_headers(),
                        params=params
                    )
                    if response.status_code == 200:
                        data = response.json()
                        st.success("Query processed successfully!")
                        st.write(data.get("result", "No result available."))
                    elif response.status_code == 401:
                        if refresh_access_token():
                            response = requests.get(
                                query_url,
                                headers=get_headers(),
                                params=params
                            )
                            if response.status_code == 200:
                                data = response.json()
                                st.success("Query processed successfully!")
                                st.write(data.get("result", "No result available."))
                            else:
                                st.error("Failed to process query after refreshing token.")
                        else:
                            st.error("Authentication failed.")
                    else:
                        error_detail = response.json().get("detail", "Failed to process query.")
                        st.error(error_detail)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a query.")