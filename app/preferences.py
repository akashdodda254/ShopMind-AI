import streamlit as st

from database.preferences import (
    get_preferences,
    save_preferences,
)


def render_preferences():

    st.title("🎯 My Shopping Preferences")

    st.write(
        "Customize your shopping interests to receive "
        "more relevant product recommendations."
    )

    current_user = st.session_state.get("current_user")

    if not current_user:
        st.warning("Please log in to manage your preferences.")
        return

    user_id = current_user["id"]

    # Load saved preferences
    preferences = get_preferences(user_id)

    st.divider()

    # Preferred Categories
    st.subheader("📦 Preferred Categories")

    categories = st.multiselect(
        "Select your favourite product categories",
        [
            "Laptop",
            "Smartphone",
            "Headphones",
            "Smartwatch",
        ],
        default=preferences["categories"],
        key="preference_categories",
    )

    # Favourite Brands
    st.subheader("🏷️ Favourite Brands")

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
        "Select your preferred brands",
        available_brands,
        default=preferences["brands"],
        key="preference_brands",
    )

    # Keywords
    st.subheader("🔎 Shopping Interests")

    keyword_text = st.text_input(
        "Enter interests separated by commas",
        value=", ".join(preferences["keywords"]),
        placeholder="Gaming, Photography, Battery life",
    )

    keywords = [
        word.strip()
        for word in keyword_text.split(",")
        if word.strip()
    ]

    # Budget
    st.subheader("💰 Shopping Budget")

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
            value=max(1000, min(int(previous_budget), 150000)),
            step=1000,
        )

    # Minimum Rating
    st.subheader("⭐ Minimum Product Rating")

    min_rating = st.slider(
        "Preferred minimum rating",
        min_value=0.0,
        max_value=5.0,
        value=float(preferences["min_rating"]),
        step=0.5,
    )

    st.divider()

    # Save Preferences
    if st.button(
        "💾 Save My Preferences",
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

        save_preferences(user_id, updated_preferences)

        st.success("Your shopping preferences have been saved!")
        st.rerun()