import os
import streamlit as st
#from dotenv import load_dotenv

# Load environment variables from .env
#load_dotenv()

# Retrieve the API key from the environment variable
#deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
#langchain_key = os.getenv("LANGCHAIN_API_KEY")
deepseek_api_key = st.secrets["deepseek"]["key"]
langchain_key = st.secrets["langchain"]["key"]
# Check if the API key is set
if deepseek_api_key is None and langchain_key is None:
    st.error("Error: DEEPSEEK_API_KEY environment variable not set.")
    st.stop() # stops the app if there is no key

# Set it so that you are able to use in the python code in other file
os.environ["LANGCHAIN_API_KEY"] = langchain_key
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "SANITY_ANAYSIS"
os.environ["DEEPSEEK_API_KEY"] = deepseek_api_key

# Rest of your code...
os.environ["STREAMLIT_SERVER_MAX_UPLOAD_SIZE"] = "2000"

# Set Streamlit to wide mode
st.set_page_config(layout="wide", page_title="Main Dashboard", page_icon="📊")


data_visualisation_page = st.Page(
    "./Pages/python_visualization_agent.py", title="Data Visualisation", icon="📈"
)

pg = st.navigation(
    {
        "Visualisation Agent": [data_visualisation_page]
    }
)

pg.run()