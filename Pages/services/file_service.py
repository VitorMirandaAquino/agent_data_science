from pathlib import Path
from typing import List, Optional
import pandas as pd
from ..config import UPLOADS_DIR, ALLOWED_EXTENSIONS

class FileService:
    @staticmethod
    def save_uploaded_file(file_data: bytes, filename: str) -> Path:
        """Save an uploaded file to the uploads directory."""
        file_path = UPLOADS_DIR / filename
        file_path.write_bytes(file_data)
        return file_path

    @staticmethod
    def get_available_files() -> List[Path]:
        """Get list of available CSV files in the uploads directory."""
        return [f for f in UPLOADS_DIR.glob("*") if f.suffix.lower() in ALLOWED_EXTENSIONS]

    @staticmethod
    def load_dataframe(file_path: Path) -> pd.DataFrame:
        """Load a CSV file into a pandas DataFrame with error handling."""
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise ValueError(f"Error loading {file_path.name}: {str(e)}")

    @staticmethod
    def delete_file(file_path: Path) -> bool:
        """Delete a file from the uploads directory."""
        try:
            file_path.unlink()
            return True
        except Exception:
            return False

    @staticmethod
    def get_file_info(file_path: Path) -> dict:
        """Get basic information about a file."""
        return {
            "name": file_path.name,
            "size": file_path.stat().st_size
        } 