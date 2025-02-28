import streamlit as st
from .components.data_management import render_data_management_tab
from .components.chat_interface import render_chat_interface
from .components.debug_interface import render_debug_interface
from .config import APP_TITLE

st.title(APP_TITLE)

# Create main tabs
tab1, tab2, tab3 = st.tabs(["Data Management", "Chat Interface", "Debug"])

# Render each tab's content
with tab1:
    render_data_management_tab()

with tab2:
    render_chat_interface()

with tab3:
    render_debug_interface()