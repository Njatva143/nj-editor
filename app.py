import streamlit as st
from auth import create_user_table, register_user, login_user
import fitz
from io import BytesIO

create_user_table()

st.set_page_config(page_title="NJ Editor", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.title("🔐 NJ Editor Login")

    menu = ["Login", "Signup"]
    choice = st.selectbox("Select Option", menu)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Signup":
        if st.button("Create Account"):
            if register_user(username, password):
                st.success("Account Created")
            else:
                st.error("Username already exists")

    if choice == "Login":
        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid Credentials")

def dashboard():
    st.sidebar.success(f"Welcome {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("📄 NJ Editor Dashboard")

    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

    if uploaded_file:
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page = doc[0]
        pix = page.get_pixmap()
        img_bytes = pix.tobytes("png")
        st.image(img_bytes)

        text = st.text_input("Add Text")
        if st.button("Apply Text"):
            page.insert_text((50, 50), text, fontsize=20)
            edited_pdf = BytesIO()
            doc.save(edited_pdf)
            edited_pdf.seek(0)
            st.download_button("Download PDF", edited_pdf, "edited.pdf")

if not st.session_state.logged_in:
    login_page()
else:
    dashboard()
