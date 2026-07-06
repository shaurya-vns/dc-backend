import streamlit as st

if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

st.set_page_config(layout="wide")

st.title("🍱 Dashboard")

st.write("Welcome", st.session_state["user"]["name"])

st.sidebar.success("Admin")

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.switch_page("app.py")