import streamlit as st

from database.users import get_user_by_id, change_password


def render_profile():

    st.title("👤 My Profile")
    st.write("Manage your ShopMind account.")

    current_user = st.session_state.get("current_user")

    if not current_user:
        st.warning("Please log in to view your profile.")
        return

    user = get_user_by_id(current_user["id"])

    if not user:
        st.error("Unable to retrieve your account details.")
        return

    # Account Information
    st.subheader("📋 Account Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Username:** {user['username']}")
        st.write(f"**Email:** {user['email']}")

    with col2:
        st.write(f"**User ID:** {user['id']}")
        st.write(f"**Member Since:** {user['created_at']}")

    st.divider()

    # Password Management
    st.subheader("🔐 Change Password")

    with st.form("change_password_form"):

        current_password = st.text_input(
            "Current Password",
            type="password",
        )

        new_password = st.text_input(
            "New Password",
            type="password",
        )

        confirm_password = st.text_input(
            "Confirm New Password",
            type="password",
        )

        submitted = st.form_submit_button(
            "Update Password",
            use_container_width=True,
        )

        if submitted:

            if not current_password or not new_password or not confirm_password:
                st.warning("Please complete all password fields.")

            elif new_password != confirm_password:
                st.error("New passwords do not match.")

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

    st.divider()

    st.subheader("🛡️ Account Security")

    st.info(
        "ShopMind uses bcrypt password hashing. "
        "Your original password is never stored in plain text."
    )