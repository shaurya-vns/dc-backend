import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api/dashboard/login/"   # Change to your API

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="🍱",
    layout="centered"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

username = st.text_input("Phone Number")
password = st.text_input("Password", type="password")

if st.button("Login"):

    payload = {
        "phoneNumber": username,
        "password": password
    }

    try:
        response = requests.post(API_URL, json=payload)
        result = response.json()

        if response.status_code == 200 and result["statusCode"] == 1:

            st.session_state.logged_in = True
            st.session_state.token = result["responseData"]["token"]
            st.session_state.user = result["responseData"]["data"]

            st.success(result["responseData"]["message"])

            st.switch_page("pages/dashboard.py")

        else:
            message = result.get("responseData", {}).get(
                "message",
                "Login failed"
            )
            st.error(message)

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to Django server.")

    except Exception as e:
        st.error(str(e))