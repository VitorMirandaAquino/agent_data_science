import streamlit as st

def render_debug_interface():
    """Render the debug interface tab content."""
    if 'visualisation_chatbot' in st.session_state:
        st.subheader("Intermediate Outputs")
        
        for i, output in enumerate(st.session_state.visualisation_chatbot.intermediate_outputs):
            with st.expander(f"Step {i+1}"):
                if isinstance(output, str):
                    st.text(output)
                else:
                    if 'thought' in output:
                        st.markdown("### Thought Process")
                        st.markdown(output['thought'])
                    if 'code' in output:
                        st.markdown("### Code")
                        st.code(output['code'], language="python")
                    if 'output' in output:
                        st.markdown("### Output")
                        st.text(output['output'])
    else:
        st.info("No debug information available yet. Start a conversation to see intermediate outputs.") 