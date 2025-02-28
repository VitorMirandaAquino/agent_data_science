import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from ..backend import PythonChatbot, InputData
from ..config import CHAT_CONTAINER_HEIGHT, UPLOADS_DIR
from pathlib import Path

def render_chat_interface():
    """Render the chat interface tab content."""
    if 'selected_files' in st.session_state and st.session_state['selected_files']:
        if 'visualisation_chatbot' not in st.session_state:
            st.session_state.visualisation_chatbot = PythonChatbot()
            
        chat_container = st.container(height=CHAT_CONTAINER_HEIGHT)
        
        with chat_container:
            # Display chat history
            for msg in st.session_state.visualisation_chatbot.chat_history:
                if isinstance(msg, HumanMessage):
                    st.chat_message("You").markdown(msg.content)
                elif isinstance(msg, AIMessage):
                    if 'tool_calls' not in msg.additional_kwargs:
                        st.chat_message("AI").markdown(msg.content)
        
        # Chat input
        st.chat_input(
            placeholder="Ask me anything about your data",
            on_submit=_handle_user_input,
            key='user_input'
        )
    else:
        st.info("Please select files to analyze in the Data Management tab first.")

def _handle_user_input():
    """Handle user input in the chat interface."""
    user_query = st.session_state['user_input']
    selected_files = st.session_state['selected_files']
    
    input_data_list = [
        InputData(
            variable_name=Path(file).stem,
            data_path=str(Path(UPLOADS_DIR) / file)
        )
        for file in selected_files
    ]
    
    st.session_state.visualisation_chatbot.user_sent_message(
        user_query,
        input_data=input_data_list
    ) 