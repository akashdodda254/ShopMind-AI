import streamlit as st

from database.db import get_product_by_id
from database.wishlist import add_to_wishlist
from database.cart import add_to_cart
from recommendation.engine import RecommendationEngine


def render_product_details():

    product_id = st.session_state.get("selected_product_id")

    if not product_id:
        st.warning("Please select a product to view its details.")
        return

    product = get_product_by_id(product_id)

    if not product:
        st.error("Product not found.")
        return

    current_user = st.session_state.get("current_user")

    # -----------------------------------------
    # PRODUCT HEADER
    # -----------------------------------------

    st.title(product["name"])

    st.caption(
        f"{product['brand']} · {product['category']}"
    )

    st.divider()

    # -----------------------------------------
    # PRODUCT INFORMATION
    # -----------------------------------------

    left, right = st.columns([1, 1])

    with left:

        st.markdown("### Product Overview")

        st.markdown(
            f"""
            <div style="
                background: #F5F7FC;
                padding: 25px;
                border-radius: 15px;
                text-align: center;
            ">
                <div style="font-size: 75px;">🛍️</div>
                <div style="font-size: 14px; color: #777;">
                    {product['category']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:

        st.markdown("### Product Information")

        st.markdown(
            f"## ₹{product['price']:,.0f}"
        )

        st.write(
            f"⭐ **{product['rating']}/5** "
            f"({product['rating_count']} ratings)"
        )

        st.write(
            f"**Brand:** {product['brand']}"
        )

        if product["stock"] > 0:
            st.success(f"In Stock: {product['stock']} units")
        else:
            st.error("Currently Out of Stock")

        st.write(product.get("description", ""))

        # -----------------------------------------
        # CUSTOMER ACTIONS
        # -----------------------------------------

        if current_user:

            st.divider()

            if st.button(
                "❤️ Add to Wishlist",
                use_container_width=True
            ):

                success, message = add_to_wishlist(
                    current_user["id"],
                    product["id"]
                )

                if success:
                    st.success(message)
                else:
                    st.info(message)

            if product["stock"] > 0:

                quantity = st.number_input(
                    "Quantity",
                    min_value=1,
                    max_value=product["stock"],
                    value=1,
                    key=f"detail_quantity_{product['id']}"
                )

                if st.button(
                    "🛒 Add to Cart",
                    use_container_width=True
                ):

                    success, message = add_to_cart(
                        current_user["id"],
                        product["id"],
                        quantity
                    )

                    if success:
                        st.success(message)
                    else:
                        st.warning(message)

    # -----------------------------------------
    # TECHNICAL SPECIFICATIONS
    # -----------------------------------------

    st.divider()

    st.markdown("## ⚙️ Technical Specifications")

    specifications = product.get("specifications", "")

    if specifications:

        for specification in specifications.split(";"):

            st.markdown(f"- {specification.strip()}")

    else:

        st.info("Specifications are not available.")

    # -----------------------------------------
    # RELATED PRODUCTS
    # -----------------------------------------

    st.divider()

    st.markdown("## 🎯 Related Products")

    engine = RecommendationEngine()

    related_products = engine.recommend(
        category=product["category"],
        min_rating=0,
        limit=10
    )

    # Exclude currently viewed product
    related_products = [
        item for item in related_products
        if item["id"] != product["id"]
    ][:4]

    if not related_products:

        st.info("No related products found.")

    else:

        columns = st.columns(2)

        for index, item in enumerate(related_products):

            with columns[index % 2]:

                with st.container(border=True):

                    st.markdown(f"### {item['name']}")

                    st.caption(item["brand"])

                    st.markdown(
                        f"**₹{item['price']:,.0f}**"
                    )

                    st.write(
                        f"⭐ {item['rating']}/5"
                    )

                    if st.button(
                        "View Details",
                        key=f"related_{item['id']}",
                        use_container_width=True
                    ):

                        st.session_state.selected_product_id = item["id"]
                        st.rerun()