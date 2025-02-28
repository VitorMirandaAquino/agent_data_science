import os
import streamlit as st
from dotenv import load_dotenv
from Pages.config import STREAMLIT_CONFIG, MAX_UPLOAD_SIZE_MB

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
langchain_key = os.getenv("LANGCHAIN_API_KEY")

# Check if API keys are set
if deepseek_api_key is None and langchain_key is None:
    st.error("Error: API keys not found in .env file. Please create a .env file with DEEPSEEK_API_KEY and LANGCHAIN_API_KEY.")
    st.stop()

# Set environment variables
os.environ.update({
    "LANGCHAIN_API_KEY": langchain_key,
    "LANGCHAIN_TRACING_V2": "true",
    "LANGCHAIN_PROJECT": "SANITY_ANALYSIS",
    "DEEPSEEK_API_KEY": deepseek_api_key,
    "STREAMLIT_SERVER_MAX_UPLOAD_SIZE": str(MAX_UPLOAD_SIZE_MB)
})

# Configure Streamlit page
st.set_page_config(**STREAMLIT_CONFIG)

# Load visualization agent page
data_visualisation_page = st.Page(
    "Pages/python_visualization_agent.py",
    title="Data Visualisation",
    icon="📈"
)

# Set up navigation
pg = st.navigation(
    {
        "Visualisation Agent": [data_visualisation_page]
    }
)

pg.run()