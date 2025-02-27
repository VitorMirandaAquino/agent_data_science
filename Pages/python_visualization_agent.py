import streamlit as st
import pandas as pd
import os
import json
from langchain_core.messages import HumanMessage, AIMessage
from Pages.backend import PythonChatbot, InputData
import pickle

# Create uploads directory if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

st.title("Data Analysis Dashboard")

tab1, tab2, tab3 = st.tabs(["Data Management", "Chat Interface", "Debug"])

with tab1:
    # File upload section
    uploaded_files = st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)

    if uploaded_files:
        # Save uploaded files
        for file in uploaded_files:
            with open(os.path.join("uploads", file.name), "wb") as f:
                f.write(file.getbuffer())
        st.success("Files uploaded successfully!")

    # Get list of available CSV files
    available_files = [f for f in os.listdir("uploads") if f.endswith('.csv')]

    if available_files:
        # File selection
        selected_files = st.multiselect(
            "Select files to analyze",
            available_files,
            key="selected_files"
        )
        
        if selected_files:
            # Create tabs for each selected file
            file_tabs = st.tabs(selected_files)
            
            # Display dataframe previews and data dictionary info in tabs
            for tab, filename in zip(file_tabs, selected_files):
                with tab:
                    try:
                        df = pd.read_csv(os.path.join("uploads", filename))
                        st.write(f"Preview of {filename}:")
                        st.dataframe(df.head())
                                
                    except Exception as e:
                        st.error(f"Error loading {filename}: {str(e)}")
    
    else:
        st.info("No CSV files available. Please upload some files first.")

with tab2:
    def on_submit_user_query():
        user_query = st.session_state['user_input']
        input_data_list = [
            InputData(
                variable_name=f"{file.split('.')[0]}", 
                data_path=os.path.abspath(os.path.join("uploads", file))
            ) 
            for file in selected_files
        ]
        st.session_state.visualisation_chatbot.user_sent_message(user_query, input_data=input_data_list)

    if 'selected_files' in st.session_state and st.session_state['selected_files']:
        if 'visualisation_chatbot' not in st.session_state:
            st.session_state.visualisation_chatbot = PythonChatbot()
        chat_container = st.container(height=500)
        with chat_container:
            # Display chat history with associated images
            for msg_index, msg in enumerate(st.session_state.visualisation_chatbot.chat_history):
                msg_col, img_col = st.columns([2, 1])
                
                with msg_col:
                    if isinstance(msg, HumanMessage):
                        st.chat_message("You").markdown(msg.content)
                    elif isinstance(msg, AIMessage):
                        if 'tool_calls' not in msg.additional_kwargs:
                            st.chat_message("AI").markdown(msg.content)
        # Chat input
        st.chat_input(placeholder="Ask me anything about your data", on_submit=on_submit_user_query, key='user_input')
    else:
        st.info("Please select files to analyze in the Data Management tab first.")

with tab3:
    if 'visualisation_chatbot' in st.session_state:
        st.subheader("Intermediate Outputs")
        for i, output in enumerate(st.session_state.visualisation_chatbot.intermediate_outputs):
            with st.expander(f"Step {i+1}"):
                if 'thought' in output:
                    st.markdown("### Thought Process")
                    st.markdown(output['thought'])
                if 'code' in output:
                    st.markdown("### Code")
                    st.code(output['code'], language="python")
                if 'output' in output:
                    st.markdown("### Output")
                    st.text(output['output'])
                else:
                    st.markdown("### Output")
                    st.text(output)
        st.info("No debug information available yet. Start a conversation to see intermediate outputs.")