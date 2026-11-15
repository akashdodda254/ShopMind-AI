import streamlit as st

from recommendation.personalized_engine import PersonalizedRecommendationEngine
from database.preferences import get_preferences
from database.history import learn_preferences
from database.wishlist import add_to_wishlist
from database.cart import add_to_cart


def render_recommendation_controls():

    st.write("Discover products selected around your interests.")

    if st.button(
        "🎯 Generate My Recommendations",
        use_container_width=True,
    ):

        current_user = st.session_state.get("current_user")

        if not current_user:
            st.warning("Please log in first.")
            return

        user_id = current_user["id"]

        preferences = get_preferences(user_id)

        learned = learn_preferences(user_id=str(user_id))

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

    st.markdown("## 🎯 Recommended for You")

    st.caption(
        "Product suggestions based on your saved preferences "
        "and shopping interests."
    )

    columns = st.columns(2)

    current_user = st.session_state.get("current_user")

    for index, item in enumerate(recommendations):

        product = item["product"]
        score = item["score"]

        with columns[index % 2]:

            with st.container(border=True):

                # Recommendation badge
                st.markdown(
                    """
                    <div style="
                        display: inline-block;
                        background: #F0EDFF;
                        color: #5548E8;
                        padding: 5px 11px;
                        border-radius: 20px;
                        font-size: 11px;
                        font-weight: 700;
                        letter-spacing: 0.5px;
                    ">
                        ✨ PERSONALIZED PICK
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(f"### {product['name']}")

                st.caption(
                    f"{product.get('brand', 'N/A')} · "
                    f"{product.get('category', 'Product')}"
                )

                # Price and rating
                price_col, rating_col = st.columns(2)

                with price_col:
                    st.markdown(
                        f"""
                        <div style="
                            color: #5548E8;
                            font-size: 25px;
                            font-weight: 800;
                            padding-top: 8px;
                        ">
                            ₹{product['price']:,.0f}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with rating_col:
                    st.metric(
                        "Customer Rating",
                        f"⭐ {product.get('rating', 0)}/5",
                    )

                # Description
                st.write(
                    product.get(
                        "description",
                        "No description available."
                    )
                )

                # Recommendation score
                st.progress(
                    max(0.0, min(float(score), 1.0)),
                    text=f"Recommendation score: {score:.2f}",
                )

                # Stock
                stock = product.get("stock", 0)

                if stock > 5:
                    st.success(f"● In Stock ({stock} available)")
                elif stock > 0:
                    st.warning(f"● Only {stock} left")
                else:
                    st.error("● Out of Stock")

                # User actions
                if current_user:

                    st.divider()

                    if st.button(
                        "❤️ Add to Wishlist",
                        key=f"recommendation_wishlist_{product['id']}",
                        use_container_width=True,
                    ):

                        success, message = add_to_wishlist(
                            current_user["id"],
                            product["id"],
                        )

                        if success:
                            st.success(message)
                        else:
                            st.info(message)

                    if stock > 0:

                        quantity = st.number_input(
                            "Quantity",
                            min_value=1,
                            max_value=max(1, stock),
                            value=1,
                            key=f"recommendation_quantity_{product['id']}",
                        )

                        if st.button(
                            "🛒 Add to Cart",
                            key=f"recommendation_cart_{product['id']}",
                            use_container_width=True,
                        ):

                            success, message = add_to_cart(
                                current_user["id"],
                                product["id"],
                                quantity,
                            )

                            if success:
                                st.success(message)
                            else:
                                st.warning(message)