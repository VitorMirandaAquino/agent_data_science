import os
from pathlib import Path
import shutil
import time

# Get the base directory (where your main.py is located)
BASE_DIR = Path(__file__).parent.parent

# Define all directory paths
UPLOADS_DIR = BASE_DIR / "uploads"
FIGURES_DIR = BASE_DIR / "images" / "plotly_figures" / "pickle"

# Create necessary directories
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# App settings
APP_TITLE = "Data Analysis Dashboard"
APP_ICON = "📊"
STREAMLIT_CONFIG = {
    "layout": "wide",
    "page_title": APP_TITLE,
    "page_icon": APP_ICON,
}

# File settings
ALLOWED_EXTENSIONS = [".csv"]
MAX_UPLOAD_SIZE_MB = 2000

# Model settings
MODEL_CONFIG = {
    "temperature": 0,
    "max_tokens": None,
    "timeout": None,
    "max_retries": 2,
}

# Chat settings
CHAT_CONTAINER_HEIGHT = 400

# Add visualization settings
VIZ_SETTINGS = {
    "max_figures_per_session": 50,
    "figure_width": "100%",
    "cache_figures": True
}

# Add data settings
DATA_SETTINGS = {
    "max_file_size_mb": 100,
    "allowed_extensions": [".csv"],
    "encoding": "utf-8"
}

# Make sure to export all necessary variables
__all__ = [
    'BASE_DIR',
    'UPLOADS_DIR',
    'FIGURES_DIR',
    'CHAT_CONTAINER_HEIGHT'
]

# Ensure all required directories exist
def ensure_directories():
    """Ensure all required directories exist."""
    directories = [UPLOADS_DIR, FIGURES_DIR]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# Clean up and recreate figures directory
def clean_figures_directory():
    """Clean up the figures directory."""
    if FIGURES_DIR.exists():
        for file in FIGURES_DIR.glob("*.pickle"):
            try:
                file.unlink()
            except Exception as e:
                print(f"Could not remove file {file}: {e}")

# Initialize directories
ensure_directories()
clean_figures_directory() 