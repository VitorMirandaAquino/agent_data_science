from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL

from langchain_core.messages import AIMessage
from typing import Annotated, Tuple
from langgraph.prebuilt import InjectedState
import sys
from io import StringIO
import os
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
import pandas as pd


repl = PythonREPL()

persistent_vars = {}
plotly_saving_code = """import pickle
import uuid
import plotly

for figure in plotly_figures:
    pickle_filename = f"images/plotly_figures/pickle/{uuid.uuid4()}.pickle"
    with open(pickle_filename, 'wb') as f:
        pickle.dump(figure, f)
"""

@tool(parse_docstring=True)
def complete_python_task_no_plots(
        graph_state: Annotated[dict, InjectedState], thought: str, python_code: str
) -> Tuple[str, dict]:
    """Executes a Python task without handling plot outputs.

    Args:
        thought: Internal thought about the next action to be taken, and the reasoning behind it. This should be formatted in MARKDOWN and be high quality.
        python_code: Python code to be executed to perform analyses or create a new dataset.
    """
    # Retrieve or initialize the current variable state.
    current_variables = graph_state.get("current_variables", {})
    for input_dataset in graph_state.get("input_data", []):
        if input_dataset.variable_name not in current_variables:
            current_variables[input_dataset.variable_name] = pd.read_csv(input_dataset.data_path)

    try:
        # Capture standard output.
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        # Prepare execution globals.
        exec_globals = globals().copy()
        exec_globals.update(persistent_vars)
        exec_globals.update(current_variables)

        # Execute the provided code.
        exec(python_code, exec_globals)
        persistent_vars.update({k: v for k, v in exec_globals.items() if k not in globals()})

        # Retrieve captured output.
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        updated_state = {
            "intermediate_outputs": [{
                "thought": thought,
                "code": python_code,
                "output": output
            }],
            "current_variables": persistent_vars
        }
        return output, updated_state

    except Exception as e:
        return str(e), {
            "intermediate_outputs": [{
                "thought": thought,
                "code": python_code,
                "output": str(e)
            }]
        }


@tool(parse_docstring=True)
def complete_plot_python_task(
        graph_state: Annotated[dict, InjectedState], thought: str, python_code: str
) -> Tuple[str, dict]:
    """Executes a Python task that include generating Plotly visualizations.

    Args:
        thought: Internal thought about the next action to be taken, and the reasoning behind it. This should be formatted in MARKDOWN and be high quality.
        python_code: Python code to be executed to perform analyses, create a new dataset or create a visualization.
    """
    # Retrieve or initialize the current variable state.
    current_variables = graph_state.get("current_variables", {})
    for input_dataset in graph_state.get("input_data", []):
        if input_dataset.variable_name not in current_variables:
            current_variables[input_dataset.variable_name] = pd.read_csv(input_dataset.data_path)

    # Ensure the directory for saving plot images exists.
    if not os.path.exists("images/plotly_figures/pickle"):
        os.makedirs("images/plotly_figures/pickle")
    current_image_pickle_files = os.listdir("images/plotly_figures/pickle")

    try:
        # Capture standard output.
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        # Prepare execution globals.
        exec_globals = globals().copy()
        exec_globals.update(persistent_vars)
        exec_globals.update(current_variables)
        # Initialize an empty list to collect Plotly figures.
        exec_globals.update({"plotly_figures": []})

        # Execute the provided code.
        exec(python_code, exec_globals)
        persistent_vars.update({k: v for k, v in exec_globals.items() if k not in globals()})

        # Retrieve captured output.
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        updated_state = {
            "intermediate_outputs": [{
                "thought": thought,
                "code": python_code,
                "output": output
            }],
            "current_variables": persistent_vars
        }

        # If Plotly figures were created, execute the saving code.
        if 'plotly_figures' in exec_globals:
            exec(plotly_saving_code, exec_globals)
            # Check for newly created image files.
            new_image_folder_contents = os.listdir("images/plotly_figures/pickle")
            new_image_files = [file for file in new_image_folder_contents if file not in current_image_pickle_files]
            if new_image_files:
                updated_state["output_image_paths"] = new_image_files
            persistent_vars["plotly_figures"] = []

        return output, updated_state

    except Exception as e:
        return str(e), {
            "intermediate_outputs": [{
                "thought": thought,
                "code": python_code,
                "output": str(e)
            }]
        }
