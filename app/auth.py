import streamlit as st

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


def render_authentication():

    initialize_authentication()

    if st.session_state.logged_in:
        return True

    st.title("🛍️ Welcome to ShopMind AI")
    st.caption("Your intelligent personal shopping assistant.")

    login_tab, register_tab = st.tabs(
        ["Login", "Create Account"]
    )

    # LOGIN FORM
    with login_tab:

        st.subheader("Welcome Back!")

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

    # REGISTRATION FORM
    with register_tab:

        st.subheader("Create Your Account")

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

    return False


def render_logout():

    if st.button("Logout", use_container_width=True):

        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.messages = []

        st.rerun()