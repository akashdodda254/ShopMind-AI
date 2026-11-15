import streamlit as st

from database.preferences import (
    get_preferences,
    save_preferences,
)


def render_preferences():

    st.markdown("# 🎯 My Shopping Preferences")

    st.caption(
        "Personalize ShopMind to discover products that match "
        "your interests, brands, and budget."
    )

    current_user = st.session_state.get("current_user")

    if not current_user:
        st.warning("Please log in to manage your preferences.")
        return

    user_id = current_user["id"]

    preferences = get_preferences(user_id)

    # -----------------------------------------
    # PREFERENCES HEADER
    # -----------------------------------------

    st.markdown(
        """
        <div style="
            background: linear-gradient(120deg, #5548E8, #8177FF, #38BDF8);
            padding: 25px;
            border-radius: 16px;
            margin: 15px 0 25px 0;
        ">
            <h2 style="color:white; margin:0;">
                Make Shopping Personal ✨
            </h2>
            <p style="color:rgba(255,255,255,0.9); margin:8px 0 0 0;">
                Your preferences help ShopMind deliver more relevant
                product recommendations.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------
    # PREFERRED CATEGORIES
    # -----------------------------------------

    st.markdown("## 📦 Preferred Categories")

    st.write("Choose the product categories you enjoy exploring.")

    categories = st.multiselect(
        "Favourite product categories",
        [
            "Laptop",
            "Smartphone",
            "Headphones",
            "Smartwatch",
        ],
        default=preferences["categories"],
        key="preference_categories",
    )

    st.divider()

    # -----------------------------------------
    # FAVOURITE BRANDS
    # -----------------------------------------

    st.markdown("## 🏷️ Favourite Brands")

    st.write("Select the brands you prefer.")

    available_brands = [
        "Apple",
        "Samsung",
        "OnePlus",
        "Google",
        "ASUS",
        "Acer",
        "HP",
        "Sony",
        "Bose",
        "JBL",
    ]

    brands = st.multiselect(
        "Preferred brands",
        available_brands,
        default=preferences["brands"],
        key="preference_brands",
    )

    st.divider()

    # -----------------------------------------
    # SHOPPING INTERESTS
    # -----------------------------------------

    st.markdown("## 🔎 Shopping Interests")

    keyword_text = st.text_input(
        "What features or interests matter to you?",
        value=", ".join(preferences["keywords"]),
        placeholder="Gaming, Photography, Battery life",
    )

    keywords = list(dict.fromkeys(
        word.strip()
        for word in keyword_text.split(",")
        if word.strip()
    ))

    st.caption(
        "Separate multiple interests using commas."
    )

    st.divider()

    # -----------------------------------------
    # SHOPPING BUDGET
    # -----------------------------------------

    st.markdown("## 💰 Shopping Budget")

    has_budget = st.checkbox(
        "Set a maximum shopping budget",
        value=preferences["max_budget"] is not None,
    )

    max_budget = None

    if has_budget:

        previous_budget = preferences["max_budget"] or 50000

        max_budget = st.slider(
            "Maximum budget (₹)",
            min_value=1000,
            max_value=150000,
            value=max(
                1000,
                min(int(previous_budget), 150000),
            ),
            step=1000,
        )

        st.info(
            f"Your preferred maximum budget is ₹{max_budget:,}."
        )

    else:

        st.caption(
            "No maximum budget restriction."
        )

    st.divider()

    # -----------------------------------------
    # MINIMUM PRODUCT RATING
    # -----------------------------------------

    st.markdown("## ⭐ Product Quality Preference")

    min_rating = st.slider(
        "Minimum preferred product rating",
        min_value=0.0,
        max_value=5.0,
        value=float(preferences["min_rating"]),
        step=0.5,
    )

    st.caption(
        f"You prefer products rated at least {min_rating}/5."
    )

    st.divider()

    # -----------------------------------------
    # SAVE PREFERENCES
    # -----------------------------------------

    st.markdown("## 💾 Save Your Preferences")

    st.write(
        "ShopMind will use these preferences when generating "
        "personalized recommendations."
    )

    if st.button(
        "✨ Save My Preferences",
        use_container_width=True,
        type="primary",
    ):

        updated_preferences = {
            "categories": categories,
            "brands": brands,
            "keywords": keywords,
            "max_budget": max_budget,
            "min_rating": min_rating,
        }

        save_preferences(
            user_id,
            updated_preferences,
        )

        st.success(
            "Your shopping preferences have been saved!"
        )

        st.rerun()