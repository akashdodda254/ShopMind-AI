import streamlit as st

from database.wishlist import (
    get_wishlist,
    remove_from_wishlist,
)


def render_wishlist():

    st.markdown("# ❤️ My Wishlist")

    st.caption(
        "All your favourite products, collected in one place."
    )

    current_user = st.session_state.get("current_user")

    if not current_user:
        st.warning("Please log in to view your wishlist.")
        return

    user_id = current_user["id"]

    wishlist_products = get_wishlist(user_id)

    # -----------------------------------------
    # WISHLIST HEADER
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
                Your Favourite Finds 💜
            </h2>
            <p style="color:rgba(255,255,255,0.9); margin:8px 0 0 0;">
                Keep track of the products you love.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------
    # WISHLIST SUMMARY
    # -----------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "❤️ Saved Products",
            len(wishlist_products),
        )

    with col2:
        total_value = sum(
            product["price"]
            for product in wishlist_products
        )

        st.metric(
            "💰 Total Catalogue Value",
            f"₹{total_value:,.0f}",
        )

    st.divider()

    # -----------------------------------------
    # EMPTY WISHLIST
    # -----------------------------------------

    if not wishlist_products:

        with st.container(border=True):

            st.markdown(
                """
                <div style="
                    text-align:center;
                    padding:35px 15px;
                ">
                    <div style="font-size:55px;">💝</div>
                    <h2 style="color:#5548E8;">
                        Your Wishlist is Empty
                    </h2>
                    <p style="color:#7B8298;">
                        Discover products you love and save them here
                        for easy access later.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        return

    # -----------------------------------------
    # SAVED PRODUCTS
    # -----------------------------------------

    st.markdown("## 💝 Your Saved Products")

    columns = st.columns(2)

    for index, product in enumerate(wishlist_products):

        with columns[index % 2]:

            with st.container(border=True):

                st.markdown(
                    """
                    <div style="
                        display:inline-block;
                        background:#FFF0F4;
                        color:#E64980;
                        padding:5px 10px;
                        border-radius:20px;
                        font-size:11px;
                        font-weight:700;
                    ">
                        ❤️ SAVED TO WISHLIST
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(f"### {product['name']}")

                st.caption(
                    f"{product.get('brand', 'N/A')} · "
                    f"{product.get('category', 'Product')}"
                )

                st.markdown(
                    f"""
                    <div style="
                        color:#5548E8;
                        font-size:26px;
                        font-weight:800;
                        margin:10px 0;
                    ">
                        ₹{product['price']:,.0f}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.metric(
                    "Customer Rating",
                    f"⭐ {product['rating']}/5",
                )

                if product.get("description"):
                    st.write(product["description"])

                st.caption(
                    f"Added on: {product['wishlist_added_at']}"
                )

                st.divider()

                if st.button(
                    "🗑️ Remove from Wishlist",
                    key=f"remove_wishlist_{product['id']}",
                    use_container_width=True,
                ):

                    success, message = remove_from_wishlist(
                        user_id,
                        product["id"],
                    )

                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
