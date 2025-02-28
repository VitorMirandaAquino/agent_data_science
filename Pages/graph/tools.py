from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL

from typing import Annotated, Tuple
from langgraph.prebuilt import InjectedState
import sys
from io import StringIO
import os
import pandas as pd


repl = PythonREPL()

persistent_vars = {}

@tool(parse_docstring=True)
def complete_python_task(
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



