from pathlib import Path
import pandas as pd
from typing import Dict
from Pages.data_models import InputData

class DataManager:
    def __init__(self, uploads_dir: Path):
        self.uploads_dir = uploads_dir
        self.current_variables: Dict[str, pd.DataFrame] = {}
        
    def load_dataset(self, input_data: InputData) -> pd.DataFrame:
        """Load a dataset if not already loaded."""
        if input_data.variable_name not in self.current_variables:
            self.current_variables[input_data.variable_name] = pd.read_csv(input_data.data_path)
        return self.current_variables[input_data.variable_name]
    
    def get_all_variables(self) -> Dict[str, pd.DataFrame]:
        """Get all loaded variables."""
        return self.current_variables
    
    def clear_variables(self):
        """Clear all loaded variables."""
        self.current_variables.clear() 