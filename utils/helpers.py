import streamlit as st


def update_log(new_message=None, log_placeholder=None):
    if new_message:
        st.session_state.log_messages.append(new_message)
    
    if log_placeholder:
        log_placeholder.markdown("  \n".join(st.session_state.log_messages))
