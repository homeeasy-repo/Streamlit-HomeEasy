import streamlit as st
from pages import home, client

st.set_page_config(
    page_title="HomeEasy",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for white background and default font size
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif !important;
            font-size: 22px !important;
        }
        .main { background-color: #fff; }
        .stSidebar { background-color: #1e293b; }
        .css-1d391kg { color: #fff; }
        .stButton>button { background-color: #2563eb; color: #fff; }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Client"])

# Page routing
if page == "Home":
    home.show()
elif page == "Client":
    client.show()
