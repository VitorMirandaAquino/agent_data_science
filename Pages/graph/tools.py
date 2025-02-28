from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL
from typing import Annotated, Tuple
from langgraph.prebuilt import InjectedState
import sys
from io import StringIO
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from Pages.services import viz_manager
from Pages.services.data_manager import DataManager
from Pages.config import UPLOADS_DIR

repl = PythonREPL()
persistent_vars = {}

# Code for saving plotly figures
plotly_saving_code = """import pickle
import uuid
import plotly

for figure in plotly_figures:
    pickle_filename = f"images/plotly_figures/pickle/{uuid.uuid4()}.pickle"
    with open(pickle_filename, 'wb') as f:
        pickle.dump(figure, f)
"""

# Initialize managers
data_manager = DataManager(UPLOADS_DIR)

@tool(parse_docstring=True)
def complete_python_task(
        graph_state: Annotated[dict, InjectedState], 
        thought: str, 
        python_code: str
) -> Tuple[str, dict]:
    """Execute Python code for data analysis.

    Args:
        graph_state: The current state of the graph.
        thought: The reasoning behind the analysis.
        python_code: The Python code to execute.

    Returns:
        tuple: A tuple containing (output message, state updates)
    """
    # Retrieve or initialize the current variable state
    for input_dataset in graph_state.get("input_data", []):
        data_manager.load_dataset(input_dataset)

    try:
        # Capture standard output
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        # Prepare execution globals
        exec_globals = {
            'pd': pd,
            'np': np,
            **data_manager.get_all_variables()
        }

        # Execute the code
        exec(python_code, exec_globals)

        # Get captured output
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        return output, {
            "intermediate_outputs": [{
                "thought": thought,
                "code": python_code,
                "output": output
            }]
        }

    except Exception as e:
        return str(e), {
            "intermediate_outputs": [{
                "thought": thought,
                "code": python_code,
                "output": str(e)
            }]
        }

@tool(parse_docstring=True)
def create_visualization(
        graph_state: Annotated[dict, InjectedState], 
        thought: str, 
        python_code: str
) -> Tuple[str, dict]:
    """Create a Plotly visualization.

    Args:
        graph_state: The current state of the graph.
        thought: The reasoning behind the visualization.
        python_code: The Python code that creates the Plotly figure.

    Returns:
        tuple: A tuple containing (output message, state updates)
    """
    # Load data
    for input_dataset in graph_state.get("input_data", []):
        data_manager.load_dataset(input_dataset)
    
    # Check for existing visualization
    if existing_file := viz_manager.exists(python_code):
        return "This visualization already exists.", {
            "intermediate_outputs": [{
                "thought": "Reusing existing visualization",
                "code": python_code,
            }],
            "output_image_paths": [existing_file]
        }

    try:
        # Prepare execution globals
        exec_globals = {
            'pd': pd,
            'np': np,
            'px': px,
            'go': go,
            'plotly_figures': [],
            **data_manager.get_all_variables()
        }

        # Execute the code
        exec(python_code, exec_globals)
        
        if not exec_globals['plotly_figures']:
            raise ValueError("No figures were added to plotly_figures list")
        
        # Save the figure using the manager
        filename = viz_manager.save_figure(exec_globals['plotly_figures'][0], python_code)
        
        return "Visualization created successfully", {
            "intermediate_outputs": [{
                "thought": thought,
                "code": python_code,
            }],
            "output_image_paths": [filename]
        }

    except Exception as e:
        return str(e), {
            "intermediate_outputs": [{
                "thought": thought,
                "code": python_code,
                "output": str(e)
            }],
            "output_image_paths": []
        }



