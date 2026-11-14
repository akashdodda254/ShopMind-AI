import streamlit as st

from app.sidebar import render_sidebar
from app.profile import render_profile
from auth import render_authentication, render_logout
from dashboard import render_dashboard
from chat import render_chat
from recommendations import (
    render_recommendation_controls,
    render_personalized_recommendations,
)
from comparison_ui import render_comparison
from price_dashboard import render_price_dashboard
from review_dashboard import render_review_dashboard
from state import initialize_app_state, get_shopmind
from preferences import render_preferences
from wishlist import render_wishlist
from cart import render_cart

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ShopMind AI",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# APPLICATION STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        [data-testid="stSidebar"] {
            border-right: 1px solid rgba(128, 128, 128, 0.2);
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# INITIALIZE SHOPMIND
# --------------------------------------------------
initialize_app_state()
shopmind = get_shopmind()



# --------------------------------------------------
# AUTHENTICATION
# --------------------------------------------------

if not render_authentication():
    st.stop()


# --------------------------------------------------
# INITIALIZE USER DATA
# --------------------------------------------------



category, budget, page = render_sidebar()
# --------------------------------------------------
# MAIN PAGE ROUTING
# --------------------------------------------------

if page == "Shopping Assistant":

    render_dashboard()

    render_personalized_recommendations()

    render_chat(
        shopmind,
        category=category,
        budget=budget,
    )


elif page == "Product Comparison":

    st.title("⚖️ Product Comparison")

    render_comparison()

elif page == "My Profile":
    render_profile()    

elif page == "My Cart":
    render_cart()
    
elif page == "My Wishlist":
    render_wishlist()
    
        
elif page == "My Preferences":
    render_preferences()

elif page == "Price Tracking":

    st.title("📉 Price Tracking")

    render_price_dashboard()


elif page == "Review Analysis":

    st.title("⭐ Review Analysis")

    render_review_dashboard()