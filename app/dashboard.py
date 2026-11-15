import streamlit as st


def render_header():

    st.markdown(
        """
        <div style="margin-bottom: 25px;">
            <div style="
                color: #6C63FF;
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 2px;
                text-transform: uppercase;
            ">
                Your AI Shopping Companion
            </div>

            <h1 style="
                color: #20243A;
                font-size: 36px;
                font-weight: 800;
                margin: 5px 0;
            ">
                Discover Smarter Shopping.
            </h1>

            <p style="
                color: #7B8298;
                font-size: 16px;
                margin-top: 5px;
            ">
                Find products, compare prices, and discover recommendations
                tailored to your needs.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_welcome():

    current_user = st.session_state.get("current_user")

    username = (
        current_user.get("username", "Shopper")
        if current_user
        else "Shopper"
    )

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(120deg, #5548E8, #8177FF, #38BDF8);
            padding: 28px;
            border-radius: 18px;
            margin-bottom: 25px;
            box-shadow: 0 8px 25px rgba(108,99,255,0.18);
        ">
            <div style="
                color: rgba(255,255,255,0.8);
                font-size: 13px;
                font-weight: 600;
                letter-spacing: 1px;
            ">
                WELCOME TO SHOPMIND
            </div>

            <h2 style="
                color: white;
                font-size: 29px;
                font-weight: 800;
                margin: 8px 0;
            ">
                Hello, {username}! 👋
            </h2>

            <p style="
                color: rgba(255,255,255,0.9);
                font-size: 15px;
                margin-bottom: 0;
            ">
                Your next great purchase starts here.
                Let AI help you make a smarter decision.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dashboard():

    render_header()

    render_welcome()

    # -----------------------------------------
    # FEATURE HIGHLIGHTS
    # -----------------------------------------

    st.markdown("### ✨ Explore ShopMind")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div style="
                background: white;
                padding: 20px;
                border-radius: 14px;
                border: 1px solid #E8EAF2;
                min-height: 145px;
            ">
                <div style="font-size: 28px;">🤖</div>
                <h4 style="color:#20243A;">AI Shopping</h4>
                <p style="color:#7B8298;font-size:13px;">
                    Describe what you need and get intelligent suggestions.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div style="
                background: white;
                padding: 20px;
                border-radius: 14px;
                border: 1px solid #E8EAF2;
                min-height: 145px;
            ">
                <div style="font-size: 28px;">⚖️</div>
                <h4 style="color:#20243A;">Smart Comparison</h4>
                <p style="color:#7B8298;font-size:13px;">
                    Compare products and understand their differences.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div style="
                background: white;
                padding: 20px;
                border-radius: 14px;
                border: 1px solid #E8EAF2;
                min-height: 145px;
            ">
                <div style="font-size: 28px;">🎯</div>
                <h4 style="color:#20243A;">Personalized Picks</h4>
                <p style="color:#7B8298;font-size:13px;">
                    Discover products based on your shopping interests.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### 💡 Your Shopping Journey")

    st.info(
        "Use the AI Shopping Assistant below to describe a product, "
        "explore recommendations, or ask for help choosing between options."
    )
