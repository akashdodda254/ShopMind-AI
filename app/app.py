import streamlit as st
from pathlib import Path
from product_search import render_advanced_search
from sidebar import render_sidebar
from user_profile import render_profile
from auth import render_authentication
from dashboard import render_dashboard
from chat import render_chat
from recommendations import render_personalized_recommendations
from comparison_ui import render_comparison
from price_dashboard import render_price_dashboard
from review_dashboard import render_review_dashboard
from state import initialize_app_state, get_shopmind
from preferences import render_preferences
from wishlist import render_wishlist
from cart import render_cart
from orders import render_orders
from admin import render_admin_dashboard
from product_details import render_product_details

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
# LOAD CUSTOM CSS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSS_PATH = PROJECT_ROOT / "styles" / "main.css"


def load_css():
    if CSS_PATH.exists():
        with open(CSS_PATH, "r", encoding="utf-8") as css_file:
            st.markdown(
                f"<style>{css_file.read()}</style>",
                unsafe_allow_html=True,
            )


load_css()


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
# SIDEBAR
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

elif page == "Advanced Product Search":
    
    render_advanced_search()
elif page == "Product Details":
    
    render_product_details()    
    
elif page == "My Cart":

    render_cart()


elif page == "My Orders":

    render_orders()


elif page == "Admin Dashboard":

    render_admin_dashboard()


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