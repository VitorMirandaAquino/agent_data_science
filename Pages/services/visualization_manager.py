from pathlib import Path
import pickle
from typing import Dict, Optional
import hashlib
import plotly.graph_objects as go
from Pages.config import FIGURES_DIR

class VisualizationManager:
    def __init__(self, figures_dir: Path):
        self.figures_dir = figures_dir
        self.visualization_cache: Dict[str, str] = {}
        
    def get_hash(self, code: str) -> str:
        """Generate a hash for the visualization code."""
        return hashlib.md5(code.encode()).hexdigest()
    
    def exists(self, code: str) -> Optional[str]:
        """Check if visualization exists and return filename if it does."""
        code_hash = self.get_hash(code)
        filename = f"{code_hash}.pickle"
        if (self.figures_dir / filename).exists():
            return filename
        return None
    
    def save_figure(self, fig: go.Figure, code: str) -> str:
        """Save a plotly figure and return the filename."""
        code_hash = self.get_hash(code)
        filename = f"{code_hash}.pickle"
        filepath = self.figures_dir / filename
        
        # Ensure the directory exists
        self.figures_dir.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'wb') as f:
            pickle.dump(fig, f)
            
        return filename
    
    def load_figure(self, filename: str) -> go.Figure:
        """Load a figure from pickle file."""
        filepath = self.figures_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Figure file not found: {filepath}")
        
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    
    def clear_cache(self):
        """Clear the visualization cache."""
        self.visualization_cache.clear()

# Create the singleton instance after the class definition
viz_manager = VisualizationManager(FIGURES_DIR) 