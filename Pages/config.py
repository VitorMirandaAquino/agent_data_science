import os
from pathlib import Path
import shutil

# Base paths
BASE_DIR = Path(__file__).parent.parent
UPLOADS_DIR = BASE_DIR / "uploads"
PROMPTS_DIR = BASE_DIR / "Pages" / "prompts"
FIGURES_DIR = BASE_DIR / "images" / "plotly_figures" / "pickle"

# Clean up and recreate figures directory
if FIGURES_DIR.exists():
    shutil.rmtree(FIGURES_DIR)
FIGURES_DIR.parent.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(exist_ok=True)

# Ensure required directories exist
UPLOADS_DIR.mkdir(exist_ok=True)

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
CHAT_CONTAINER_HEIGHT = 500 