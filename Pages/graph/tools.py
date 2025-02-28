from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL
from typing import Annotated, Tuple
from langgraph.prebuilt import InjectedState
import sys
from io import StringIO
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
import pickle
import uuid

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

@tool(parse_docstring=True)
def complete_python_task(
        graph_state: Annotated[dict, InjectedState], thought: str, python_code: str
) -> Tuple[str, dict]:
    """Executes a Python task for data analysis (without visualization).

    Args:
        thought: Internal thought about what analysis needs to be done and why.
        python_code: Python code for data analysis. Should use print() for outputs.
    """
    # Retrieve or initialize the current variable state
    current_variables = graph_state.get("current_variables", {})
    for input_dataset in graph_state.get("input_data", []):
        if input_dataset.variable_name not in current_variables:
            current_variables[input_dataset.variable_name] = pd.read_csv(input_dataset.data_path)

    try:
        # Capture standard output
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        # Prepare execution globals
        exec_globals = {
            'pd': pd,
            'np': np,
            **persistent_vars,
            **current_variables
        }

        # Execute the provided code
        exec(python_code, exec_globals)
        persistent_vars.update({k: v for k, v in exec_globals.items() if k not in globals()})

        # Get captured output
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        updated_state = {
            "intermediate_outputs": [{
                "thought": thought,
                "code": python_code,
                "output": output
            }],
            "current_variables": persistent_vars,
            "output_image_paths": []
        }

        return output, updated_state

    except Exception as e:
        return str(e), {
            "intermediate_outputs": [{
                "thought": thought,
                "code": python_code,
                "output": str(e)
            }],
            "output_image_paths": []
        }

@tool(parse_docstring=True)
def create_visualization(
        graph_state: Annotated[dict, InjectedState], thought: str, python_code: str
) -> Tuple[str, dict]:
    """Creates a single data visualization using Plotly.

    Args:
        thought: Internal thought about why this specific visualization is needed and what it will show.
        python_code: Python code that creates ONE Plotly figure. Must add the figure to plotly_figures list.
    """
    # Check if this exact code was run before
    if "previous_viz_codes" not in persistent_vars:
        persistent_vars["previous_viz_codes"] = set()
    
    # If we've seen this exact code before, prevent recreation
    if python_code in persistent_vars["previous_viz_codes"]:
        return "This visualization has already been created.", {
            "intermediate_outputs": [{
                "thought": "Preventing duplicate visualization",
                "code": python_code,
                "output": "This exact visualization was already created before."
            }]
        }
    
    # Add this code to the set of previous visualizations
    persistent_vars["previous_viz_codes"].add(python_code)

    # Retrieve or initialize the current variable state
    current_variables = graph_state.get("current_variables", {})
    for input_dataset in graph_state.get("input_data", []):
        if input_dataset.variable_name not in current_variables:
            current_variables[input_dataset.variable_name] = pd.read_csv(input_dataset.data_path)

    # Create directory structure if it doesn't exist
    os.makedirs("images/plotly_figures/pickle", exist_ok=True)

    current_image_pickle_files = os.listdir("images/plotly_figures/pickle")

    try:
        exec_globals = {
            'pd': pd,
            'np': np,
            'px': px,
            'go': go,
            'plotly_figures': [],
            **persistent_vars,
            **current_variables
        }

        # Execute the provided code
        exec(python_code, exec_globals)
        
        # Verify only one figure was created
        if len(exec_globals['plotly_figures']) == 0:
            raise ValueError("No figures were added to plotly_figures list")
        if len(exec_globals['plotly_figures']) > 1:
            raise ValueError("Only one figure should be created at a time")
            
        exec(plotly_saving_code, exec_globals)
        
        # Check for new images
        new_image_folder_contents = os.listdir("images/plotly_figures/pickle")
        new_image_files = [file for file in new_image_folder_contents 
                         if file not in current_image_pickle_files]

        updated_state = {
            "intermediate_outputs": [{
                "thought": thought,
                "code": python_code,
            }],
            "current_variables": persistent_vars,
            "output_image_paths": new_image_files
        }
        
        return "Visualization created successfully", updated_state

    except Exception as e:
        return str(e), {
            "intermediate_outputs": [{
                "thought": thought,
                "code": python_code,
                "output": str(e)
            }],
            "output_image_paths": []
        }



