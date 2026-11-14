import streamlit as st

from database.cart import (
    get_cart,
    update_cart_quantity,
    remove_from_cart,
    clear_cart,
    get_cart_total,
)


def render_cart():

    st.title("🛒 My Shopping Cart")

    st.write("Review and manage your selected products.")

    current_user = st.session_state.get("current_user")

    if not current_user:
        st.warning("Please log in to view your cart.")
        return

    user_id = current_user["id"]

    cart_items = get_cart(user_id)

    # Cart Summary
    total_items = sum(item["quantity"] for item in cart_items)
    total_price = get_cart_total(user_id)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Items", total_items)

    with col2:
        st.metric("Cart Value", f"₹{total_price:,.2f}")

    st.divider()

    if not cart_items:

        st.info(
            "Your shopping cart is empty. "
            "Explore products and add items to your cart."
        )
        return

    st.subheader("📦 Your Cart Items")

    for product in cart_items:

        with st.container(border=True):

            col1, col2 = st.columns([3, 1])

            with col1:

                st.markdown(f"### {product['name']}")

                st.write(f"**Brand:** {product['brand']}")
                st.write(f"**Category:** {product['category']}")
                st.write(f"**Unit Price:** ₹{product['price']:,.2f}")
                st.write(f"**Quantity:** {product['quantity']}")
                st.write(f"**Subtotal:** ₹{product['subtotal']:,.2f}")

                st.caption(
                    f"Available stock: {product['stock']}"
                )

            with col2:

                new_quantity = st.number_input(
                    "Quantity",
                    min_value=1,
                    max_value=max(1, product["stock"]),
                    value=product["quantity"],
                    step=1,
                    key=f"cart_quantity_{product['id']}",
                )

                if st.button(
                    "Update Quantity",
                    key=f"update_cart_{product['id']}",
                    use_container_width=True,
                ):

                    success, message = update_cart_quantity(
                        user_id,
                        product["id"],
                        new_quantity,
                    )

                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

                if st.button(
                    "🗑️ Remove",
                    key=f"remove_cart_{product['id']}",
                    use_container_width=True,
                ):

                    success, message = remove_from_cart(
                        user_id,
                        product["id"],
                    )

                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

    st.divider()

    # Cart Total
    st.subheader("💰 Order Summary")

    st.write(f"**Total Items:** {total_items}")
    st.write(f"**Total Amount:** ₹{total_price:,.2f}")

    st.caption(
        "This is an estimated cart total using ShopMind catalogue prices. "
        "Taxes, shipping, and checkout are not included."
    )

    if st.button(
        "🗑️ Clear Entire Cart",
        use_container_width=True,
    ):

        clear_cart(user_id)

        st.success("Your cart has been cleared!")
        st.rerun()