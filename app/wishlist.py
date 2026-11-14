import streamlit as st

from database.wishlist import (
    get_wishlist,
    remove_from_wishlist,
)


def render_wishlist():

    st.title("❤️ My Wishlist")

    st.write("Your favourite products, saved in one place.")

    current_user = st.session_state.get("current_user")

    if not current_user:
        st.warning("Please log in to view your wishlist.")
        return

    user_id = current_user["id"]

    wishlist_products = get_wishlist(user_id)

    # Wishlist Summary
    st.metric("Saved Products", len(wishlist_products))

    st.divider()

    if not wishlist_products:
        st.info(
            "Your wishlist is empty. Explore products and save "
            "your favourites to find them here."
        )
        return

    # Display Wishlist Products
    st.subheader("💝 Your Saved Products")

    for product in wishlist_products:

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:

                st.markdown(f"### {product['name']}")

                st.write(f"**Brand:** {product['brand']}")
                st.write(f"**Category:** {product['category']}")
                st.write(f"**Price:** ₹{product['price']:,.0f}")
                st.write(f"**Rating:** ⭐ {product['rating']}/5")

                st.caption(
                    f"Added on: {product['wishlist_added_at']}"
                )

                if product.get("description"):
                    st.write(product["description"])

            with col2:

                st.write("")

                if st.button(
                    "🗑️ Remove",
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