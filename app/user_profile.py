import streamlit as st

from database.users import get_user_by_id, change_password


def render_profile():

    st.markdown("# 👤 My Profile")

    st.caption(
        "Manage your account information and security settings."
    )

    current_user = st.session_state.get("current_user")

    if not current_user:
        st.warning("Please log in to view your profile.")
        return

    user = get_user_by_id(current_user["id"])

    if not user:
        st.error("Unable to retrieve your account details.")
        return

    # -----------------------------------------
    # PROFILE HEADER
    # -----------------------------------------

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(120deg, #5548E8, #8177FF, #38BDF8);
            padding: 28px;
            border-radius: 18px;
            margin: 15px 0 25px 0;
            box-shadow: 0 8px 25px rgba(108,99,255,0.15);
        ">
            <div style="font-size: 42px;">👤</div>

            <h2 style="
                color: white;
                margin: 8px 0;
                font-weight: 800;
            ">
                {user['username']}
            </h2>

            <p style="
                color: rgba(255,255,255,0.9);
                margin: 0;
            ">
                {user['email']}
            </p>

            <div style="
                color: rgba(255,255,255,0.75);
                font-size: 12px;
                margin-top: 12px;
                letter-spacing: 1px;
            ">
                SHOPMIND MEMBER
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------
    # ACCOUNT INFORMATION
    # -----------------------------------------

    st.markdown("## 📋 Account Information")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.caption("USERNAME")

            st.markdown(f"### {user['username']}")

            st.caption("EMAIL ADDRESS")

            st.write(user["email"])

    with col2:

        with st.container(border=True):

            st.caption("USER ID")

            st.markdown(f"### #{user['id']}")

            st.caption("MEMBER SINCE")

            st.write(user["created_at"])

    # -----------------------------------------
    # PASSWORD MANAGEMENT
    # -----------------------------------------

    st.divider()

    st.markdown("## 🔐 Password Management")

    st.write(
        "Keep your account secure by updating your password regularly."
    )

    with st.container(border=True):

        with st.form("change_password_form"):

            st.markdown("### Change Your Password")

            current_password = st.text_input(
                "Current Password",
                type="password",
            )

            new_password = st.text_input(
                "New Password",
                type="password",
                help="Your new password must contain at least 8 characters.",
            )

            confirm_password = st.text_input(
                "Confirm New Password",
                type="password",
            )

            submitted = st.form_submit_button(
                "🔒 Update Password",
                use_container_width=True,
            )

            if submitted:

                if not current_password or not new_password or not confirm_password:

                    st.warning(
                        "Please complete all password fields."
                    )

                elif new_password != confirm_password:

                    st.error(
                        "New passwords do not match."
                    )

                else:

                    success, message = change_password(
                        user["id"],
                        current_password,
                        new_password,
                    )

                    if success:
                        st.success(message)
                    else:
                        st.error(message)

    # -----------------------------------------
    # ACCOUNT SECURITY
    # -----------------------------------------

    st.divider()

    st.markdown("## 🛡️ Account Security")

    with st.container(border=True):

        st.markdown("### 🔐 Password Protection")

        st.success(
            "Your passwords are protected using bcrypt hashing."
        )

        st.caption(
            "ShopMind stores hashed passwords rather than "
            "your original plain-text password."
        )