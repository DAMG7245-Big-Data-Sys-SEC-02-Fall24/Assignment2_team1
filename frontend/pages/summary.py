import streamlit as st
import requests
from utils import get_headers, API_BASE_URL, refresh_access_token

def display():
    st.title("Summary")
    st.write("This page allows you to get summaries.")

    if st.button("Get Summary"):
        with st.spinner("Fetching summary..."):
            summary_url = f"{API_BASE_URL}/summary"
            try:
                response = requests.get(summary_url, headers=get_headers())
                if response.status_code == 200:
                    data = response.json()
                    st.success("Summary fetched successfully!")
                    st.write(data.get("message", "No summary available."))
                elif response.status_code == 401:
                    # Attempt to refresh the access token
                    if refresh_access_token():
                        # Retry the request with new access token
                        response = requests.get(summary_url, headers=get_headers())
                        if response.status_code == 200:
                            data = response.json()
                            st.success("Summary fetched successfully!")
                            st.write(data.get("message", "No summary available."))
                        else:
                            st.error("Failed to fetch summary after refreshing token.")
                    else:
                        st.error("Authentication failed.")
                else:
                    error_detail = response.json().get("detail", "Failed to fetch summary.")
                    st.error(error_detail)
            except Exception as e:
                st.error(f"An error occurred: {e}")
