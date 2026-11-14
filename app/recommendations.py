import streamlit as st

from recommendation.personalized_engine import PersonalizedRecommendationEngine
from database.preferences import get_preferences
from database.history import learn_preferences
from database.wishlist import add_to_wishlist
from database.cart import add_to_cart


def render_recommendation_controls():

    st.write("Generate recommendations using your saved preferences.")

    if st.button(
        "🎯 Generate My Recommendations",
        use_container_width=True,
    ):

        current_user = st.session_state.get("current_user")

        if not current_user:
            st.warning("Please log in first.")
            return

        user_id = current_user["id"]

        # Load saved preferences
        preferences = get_preferences(user_id)

        # Learn additional interests from shopping history
        learned = learn_preferences(user_id=str(user_id))

        # Combine saved and learned preferences
        combined_preferences = {
            "categories": list(set(
                preferences.get("categories", [])
                + learned.get("categories", [])
            )),
            "brands": preferences.get("brands", []),
            "keywords": list(set(
                preferences.get("keywords", [])
                + learned.get("keywords", [])
            )),
            "max_budget": preferences.get("max_budget"),
            "min_rating": preferences.get("min_rating", 0),
        }

        # Generate recommendations
        engine = PersonalizedRecommendationEngine()

        recommendations = engine.recommend(
            combined_preferences,
            limit=5,
        )

        st.session_state["personalized_recommendations"] = recommendations

        st.success("Your personalized recommendations are ready!")


def render_personalized_recommendations():
    
    recommendations = st.session_state.get(
        "personalized_recommendations",
        [],
    )

    if not recommendations:
        return

    st.divider()
    st.subheader("🎯 Recommended for You")

    columns = st.columns(2)

    current_user = st.session_state.get("current_user")

    for index, item in enumerate(recommendations):

        product = item["product"]
        score = item["score"]

        with columns[index % 2]:

            with st.container(border=True):

                st.markdown(f"### {product['name']}")

                st.write(f"**Brand:** {product['brand']}")
                st.write(f"**Category:** {product['category']}")
                st.write(f"**Price:** ₹{product['price']:,.0f}")
                st.write(f"**Rating:** ⭐ {product['rating']}/5")

                st.caption(
                    f"Recommendation score: {score:.2f}"
                )

                # Add to Wishlist
                if current_user:

                    if st.button(
                        "❤️ Add to Wishlist",
                        key=f"recommendation_wishlist_{product['id']}",
                        use_container_width=True,
                    ):

                        from database.wishlist import add_to_wishlist

                        success, message = add_to_wishlist(
                            current_user["id"],
                            product["id"],
                        )

                        if success:
                            st.success(message)
                        else:
                            st.info(message)