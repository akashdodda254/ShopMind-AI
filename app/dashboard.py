import streamlit as st


def render_header():
    """Display the ShopMind application header."""

    col1, col2 = st.columns([4, 1])

    with col1:
        st.title("🛍️ ShopMind AI")
        st.caption("Your intelligent personal shopping assistant.")

    with col2:
        st.success("● AI Online")

    st.divider()


def render_welcome():
    """Display the welcome section when the chat is empty."""

    st.markdown("## 👋 Welcome to ShopMind!")

    st.write(
        "Find products, compare options, discover recommendations, "
        "and make smarter shopping decisions."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🔎 **Smart Search**\n\nFind products using natural language.")

    with col2:
        st.info("⚖️ **Product Comparison**\n\nCompare prices and specifications.")

    with col3:
        st.info("🎯 **Personalized Picks**\n\nDiscover recommendations based on your interests.")


def render_dashboard():
    """Render the main shopping dashboard."""

    render_header()

    if not st.session_state.get("messages"):
        render_welcome()