import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from Pages.backend import PythonChatbot, InputData
from Pages.config import UPLOADS_DIR, CHAT_CONTAINER_HEIGHT, FIGURES_DIR
from pathlib import Path
import plotly.io as pio
import pickle
import os
from Pages.services import viz_manager  # Updated import

def render_chat_interface():
    """Render the chat interface tab content."""
    if 'selected_files' in st.session_state and st.session_state['selected_files']:
        if 'visualisation_chatbot' not in st.session_state:
            st.session_state.visualisation_chatbot = PythonChatbot()
            
        chat_container = st.container(height=CHAT_CONTAINER_HEIGHT)
        
        with chat_container:
            # Display chat history and plots
            for msg_index, msg in enumerate(st.session_state.visualisation_chatbot.chat_history):
                if isinstance(msg, HumanMessage):
                    st.chat_message("You").markdown(msg.content)
                elif isinstance(msg, AIMessage):
                    if 'tool_calls' not in msg.additional_kwargs:
                        st.chat_message("AI").markdown(msg.content)
                    
                    # Display plots
                    if msg_index in st.session_state.visualisation_chatbot.output_image_paths:
                        for image_path in st.session_state.visualisation_chatbot.output_image_paths[msg_index]:
                            try:
                                # Use the visualization manager to load the figure
                                fig = viz_manager.load_figure(image_path)
                                st.plotly_chart(fig, use_container_width=True)
                            except Exception as e:
                                st.error(f"Error displaying plot: {str(e)}")
                                st.error(f"Attempted path: {FIGURES_DIR / image_path}")
        
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