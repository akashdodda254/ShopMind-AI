import streamlit as st

from agents.orchestrator import ShopMindOrchestrator
from database.history import initialize_history_table


def initialize_app_state():
    """Initialize database tables and Streamlit session state."""

    initialize_history_table()

    default_values = {
        "messages": [],
        "pending_prompt": None,
        "current_user": None,
        "logged_in": False,
        "personalized_recommendations": [],
        "comparison_analysis": None,
        "review_analysis": None,
    }

    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value


@st.cache_resource
def get_shopmind():
    """Create and cache the ShopMind orchestrator."""

    return ShopMindOrchestrator()