import streamlit as st

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Landing Page", "Search Page", "Summary Page"])

    if page == "Landing Page":
        from landing import landing_page
        landing_page()
    elif page == "Search Page":
        from pages.search import search_page
        search_page()
    elif page == "Summary Page":
        from pages.summary import summary_page
        summary_page()

if __name__ == "__main__":
    main()
