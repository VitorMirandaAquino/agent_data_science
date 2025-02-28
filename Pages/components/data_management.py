import streamlit as st
from ..services.file_service import FileService
from pathlib import Path

def render_data_management_tab():
    """Render the data management tab content."""
    # File upload section
    uploaded_files = st.file_uploader(
        "Upload CSV files",
        type="csv",
        accept_multiple_files=True
    )

    if uploaded_files:
        for file in uploaded_files:
            FileService.save_uploaded_file(file.getbuffer(), file.name)
        st.success("Files uploaded successfully!")

    # Get list of available CSV files
    available_files = FileService.get_available_files()

    if available_files:
        # File selection
        selected_files = st.multiselect(
            "Select files to analyze",
            [f.name for f in available_files],
            key="selected_files"
        )
        
        if selected_files:
            # Create tabs for each selected file
            file_tabs = st.tabs(selected_files)
            
            # Display dataframe previews and file info in tabs
            for tab, filename in zip(file_tabs, selected_files):
                with tab:
                    try:
                        file_path = Path(UPLOADS_DIR) / filename
                        df = FileService.load_dataframe(file_path)
                        file_info = FileService.get_file_info(file_path)
                        
                        # Display file info
                        st.write("File Information:")
                        st.json(file_info)
                        
                        # Display data preview
                        st.write("Data Preview:")
                        st.dataframe(df.head())
                        
                        # Display basic statistics
                        st.write("Basic Statistics:")
                        st.dataframe(df.describe())
                                
                    except Exception as e:
                        st.error(str(e))
    else:
        st.info("No CSV files available. Please upload some files first.") 