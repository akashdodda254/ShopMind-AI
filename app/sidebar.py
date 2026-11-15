import streamlit as st
from pathlib import Path
from auth import render_logout
from recommendations import render_recommendation_controls


def render_sidebar():

    with st.sidebar:

        # -----------------------------------------
        # BRANDING
        # -----------------------------------------

        logo_path = Path(__file__).resolve().parent.parent / "assets" / "logo.svg"

        if logo_path.exists():
            logo_svg = logo_path.read_text(encoding="utf-8")

            st.markdown(
                f"""
                <div style="padding: 12px 0 20px 0; text-align: center;">
                    {logo_svg}
                    <div style="
                        font-size: 11px;
                        color: #A5AAC0;
                        letter-spacing: 2px;
                        margin-top: 8px;
                    ">
                        AI SHOPPING ASSISTANT
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # -----------------------------------------
        # USER PROFILE
        # -----------------------------------------

        current_user = st.session_state.get("current_user")

        if current_user:

            st.markdown(
                f"""
                <div style="
                    background: rgba(255,255,255,0.07);
                    border: 1px solid rgba(255,255,255,0.10);
                    border-radius: 12px;
                    padding: 13px;
                    margin-bottom: 12px;
                ">
                    <div style="font-size: 12px; color: #A5AAC0;">
                        WELCOME BACK
                    </div>
                    <div style="font-size: 17px; font-weight: 700; color: white;">
                        {current_user['username']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        render_logout()

        st.divider()

        # -----------------------------------------
        # SHOPPING FILTERS
        # -----------------------------------------

        st.markdown("### 🔎 Shopping Filters")

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

        # -----------------------------------------
        # PERSONALIZED RECOMMENDATIONS
        # -----------------------------------------

        st.markdown("### 🎯 For You")

        render_recommendation_controls()

        st.divider()

        # -----------------------------------------
        # QUICK SEARCH
        # -----------------------------------------

        st.markdown("### ⚡ Quick Discover")

        quick_searches = {
            "🎮 Gaming Laptops": "Recommend gaming laptops",
            "📱 Best Smartphones": "Show me the best smartphones",
            "🎧 Wireless Headphones": "Recommend wireless headphones",
        }

        for label, prompt in quick_searches.items():

            if st.button(label, use_container_width=True):
                st.session_state.pending_prompt = prompt
                st.rerun()

        st.divider()

        # -----------------------------------------
        # NAVIGATION
        # -----------------------------------------

        navigation_options = [
            "Shopping Assistant",
            "Advanced Product Search",
            "Product Details",
            "Product Comparison",
            "Price Tracking",
            "Review Analysis",
            "My Profile",
            "My Preferences",
            "My Wishlist",
            "My Cart",
            "My Orders",
            "Admin Dashboard",
        ]

        # Handle navigation requests from other pages
        pending_page = st.session_state.pop("pending_page", None)

        default_index = 0

        if pending_page in navigation_options:
            default_index = navigation_options.index(pending_page)

        page = st.radio(
            "Navigation",
            navigation_options,
            index=default_index,
            label_visibility="collapsed",
        )
        st.divider()

        # -----------------------------------------
        # CLEAR CHAT
        # -----------------------------------------

        if st.button(
            "🗑️ Clear Chat",
            use_container_width=True,
        ):
            st.session_state.messages = []
            st.rerun()

        st.markdown(
            """
            <div style="
                text-align: center;
                color: #777F9A;
                font-size: 11px;
                padding: 15px 0 5px 0;
            ">
                ShopMind AI · Your Smart Shopping Companion
            </div>
            """,
            unsafe_allow_html=True,
        )

    return category, budget, page