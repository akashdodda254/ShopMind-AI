import streamlit as st

from auth import render_logout
from recommendations import render_recommendation_controls


def render_sidebar():

    with st.sidebar:

        st.title("🛍️ ShopMind AI")

        current_user = st.session_state.get("current_user")

        if current_user:
            st.caption(f"Welcome, {current_user['username']}!")

        render_logout()

        st.divider()

        # Shopping Filters
        st.subheader("🔎 Shopping Filters")

        category = st.selectbox(
            "Product Category",
            [
                "All Categories",
                "Laptop",
                "Smartphone",
                "Headphones",
                "Smartwatch",
            ],
        )

        budget = st.slider(
            "Maximum Budget (₹)",
            min_value=1000,
            max_value=150000,
            value=150000,
            step=1000,
        )

        st.divider()

        # Personalized Recommendations
        st.subheader("🎯 Personalized Recommendations")

        render_recommendation_controls()

        st.divider()

        # Quick Searches
        st.subheader("⚡ Quick Searches")

        if st.button("Gaming Laptops", use_container_width=True):
            st.session_state.pending_prompt = "Recommend gaming laptops"

        if st.button("Best Smartphones", use_container_width=True):
            st.session_state.pending_prompt = "Show me the best smartphones"

        if st.button("Wireless Headphones", use_container_width=True):
            st.session_state.pending_prompt = "Recommend wireless headphones"

        st.divider()

        # Navigation
        st.subheader("🧭 Navigation")

        page = st.radio(
            "Choose a section",
            [
                "Shopping Assistant",
                "Product Comparison",
                "Price Tracking",
                "Review Analysis",
                "My Profile",
                "My Preferences",
                "My Wishlist",
                "My Cart",
            ],
            label_visibility="collapsed",
        )

        st.divider()

        # Clear Chat
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    return category, budget, page