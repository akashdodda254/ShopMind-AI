import streamlit as st
from pathlib import Path

from database.users import (
    create_users_table,
    register_user,
    login_user
)


def initialize_authentication():

    create_users_table()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "current_user" not in st.session_state:
        st.session_state.current_user = None


def load_auth_styles():

    st.markdown("""
    <style>

    /* Main background */
    .stApp {
        background: #F5F7FC;
        color: #20243A;
    }

    /* Hide unnecessary Streamlit elements */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* Main login container */
    .auth-container {
        max-width: 680px;
        margin: 25px auto 10px auto;
        padding: 35px;
        background: white;
        border: 1px solid #E8EAF2;
        border-radius: 22px;
        box-shadow: 0 12px 40px rgba(35, 30, 80, 0.08);
    }

    /* Hero section */
    .auth-hero {
        text-align: center;
        padding: 15px 10px 25px 10px;
    }

    .auth-title {
        font-size: 38px;
        font-weight: 800;
        color: #20243A;
        margin-bottom: 8px;
    }

    .auth-subtitle {
        font-size: 15px;
        color: #7B8298;
    }

    /* Form headings */
    .auth-heading {
        font-size: 25px;
        font-weight: 750;
        color: #20243A;
        margin-bottom: 5px;
    }

    /* Input fields */
    .stTextInput input {
        background: #F8F9FD !important;
        border: 1px solid #E1E4EF !important;
        border-radius: 10px !important;
        color: #20243A !important;
        min-height: 45px;
    }

    .stTextInput input:focus {
        border-color: #6C63FF !important;
        box-shadow: 0 0 0 2px rgba(108, 99, 255, 0.12) !important;
    }

    /* Buttons */
    .stButton button,
    .stFormSubmitButton button {
        background: linear-gradient(100deg, #6C63FF, #38BDF8) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        min-height: 45px;
        transition: 0.2s ease;
    }

    .stButton button:hover,
    .stFormSubmitButton button:hover {
        box-shadow: 0 5px 18px rgba(108, 99, 255, 0.25);
        transform: translateY(-1px);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        border-bottom: 1px solid #E8EAF2;
    }

    .stTabs [data-baseweb="tab"] {
        color: #7B8298;
        font-weight: 650;
    }

    .stTabs [aria-selected="true"] {
        color: #6C63FF !important;
    }

    /* Labels */
    .stTextInput label {
        color: #343950 !important;
        font-weight: 600;
    }

    </style>
    """, unsafe_allow_html=True)


def render_authentication():

    initialize_authentication()

    if st.session_state.logged_in:
        return True

    load_auth_styles()

    # Load ShopMind logo
    logo_path = (
        Path(__file__).resolve().parent.parent
        / "assets"
        / "logo.svg"
    )

    st.markdown('<div class="auth-container">', unsafe_allow_html=True)

    if logo_path.exists():
        
        logo_svg = logo_path.read_text(encoding="utf-8")

        # Resize logo
        logo_svg = logo_svg.replace(
            "<svg ",
            '<svg style="width:240px; height:auto; display:block; margin:auto;" ',
            1
        )

        # Change wordmark to dark color for light background
        logo_svg = logo_svg.replace(
            'fill="white">ShopMind</text>',
            'fill="#20243A">ShopMind</text>'
        )

        st.markdown(
            f"""
            <div style="text-align:center; margin-bottom:20px;">
                {logo_svg}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div class="auth-hero">
                <div class="auth-title">
                    Welcome to ShopMind AI
                </div>
                <div class="auth-subtitle">
                    Your intelligent personal shopping assistant.
                    Discover smarter ways to shop.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    login_tab, register_tab = st.tabs(
        ["Login", "Create Account"]
    )

    # LOGIN
    with login_tab:

        st.markdown(
            '<div class="auth-heading">Welcome Back!</div>',
            unsafe_allow_html=True
        )

        st.caption("Sign in to continue your shopping journey.")

        with st.form("login_form"):

            email = st.text_input("Email Address")

            password = st.text_input(
                "Password",
                type="password"
            )

            submitted = st.form_submit_button(
                "Login",
                use_container_width=True
            )

            if submitted:

                user = login_user(email, password)

                if user:

                    st.session_state.logged_in = True
                    st.session_state.current_user = user
                    st.session_state.messages = []

                    st.rerun()

                else:
                    st.error("Invalid email or password.")

    # REGISTRATION
    with register_tab:

        st.markdown(
            '<div class="auth-heading">Create Your Account</div>',
            unsafe_allow_html=True
        )

        st.caption("Join ShopMind and make smarter shopping decisions.")

        with st.form("register_form"):

            username = st.text_input("Username")

            new_email = st.text_input("Email Address")

            new_password = st.text_input(
                "Password",
                type="password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password"
            )

            submitted = st.form_submit_button(
                "Create Account",
                use_container_width=True
            )

            if submitted:

                if new_password != confirm_password:

                    st.error("Passwords do not match.")

                else:

                    success, message = register_user(
                        username,
                        new_email,
                        new_password
                    )

                    if success:

                        st.success(message)
                        st.info("You can now log in.")

                    else:

                        st.error(message)

    st.markdown("</div>", unsafe_allow_html=True)

    return False


def render_logout():

    if st.button("Logout", use_container_width=True):

        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.messages = []

        st.rerun()