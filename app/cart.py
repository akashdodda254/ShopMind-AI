import streamlit as st

from database.cart import (
    get_cart,
    update_cart_quantity,
    remove_from_cart,
    clear_cart,
    get_cart_total,
)

from database.orders import place_order


def render_cart():

    st.markdown("# 🛒 My Shopping Cart")

    st.caption(
        "Review your selected products and complete your order."
    )

    current_user = st.session_state.get("current_user")

    if not current_user:
        st.warning("Please log in to view your cart.")
        return

    user_id = current_user["id"]

    # -----------------------------------------
    # ORDER CONFIRMATION
    # -----------------------------------------

    if st.session_state.get("order_confirmation"):

        order = st.session_state.pop("order_confirmation")

        with st.container(border=True):

            st.success(
                f"🎉 Order #{order['order_id']} placed successfully!"
            )

            st.markdown("### Thank you for shopping with ShopMind!")

            st.metric(
                "Order Amount",
                f"₹{order['total_amount']:,.2f}",
            )

            st.info(
                "Visit My Orders to view your purchase history."
            )

    cart_items = get_cart(user_id)

    total_items = sum(
        item["quantity"] for item in cart_items
    )

    total_price = get_cart_total(user_id)

    # -----------------------------------------
    # CART HEADER
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
                Your Shopping Bag 💜
            </h2>
            <p style="color:rgba(255,255,255,0.9); margin:8px 0 0 0;">
                Everything you love, ready for checkout.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------
    # CART SUMMARY
    # -----------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📦 Total Items", total_items)

    with col2:
        st.metric(
            "💰 Cart Value",
            f"₹{total_price:,.2f}",
        )

    with col3:
        st.metric(
            "🛍️ Product Types",
            len(cart_items),
        )

    st.divider()

    # -----------------------------------------
    # EMPTY CART
    # -----------------------------------------

    if not cart_items:

        with st.container(border=True):

            st.markdown(
                """
                <div style="
                    text-align:center;
                    padding:35px 15px;
                ">
                    <div style="font-size:55px;">🛒</div>
                    <h2 style="color:#5548E8;">
                        Your Cart is Empty
                    </h2>
                    <p style="color:#7B8298;">
                        Discover something amazing and add it
                        to your shopping cart.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        return

    # -----------------------------------------
    # CART PRODUCTS
    # -----------------------------------------

    st.markdown("## 📦 Your Cart Items")

    for product in cart_items:

        with st.container(border=True):

            col1, col2 = st.columns([3, 1])

            with col1:

                st.markdown(f"### {product['name']}")

                st.caption(
                    f"{product.get('brand', 'N/A')} · "
                    f"{product.get('category', 'Product')}"
                )

                st.write(
                    f"**Unit Price:** ₹{product['price']:,.2f}"
                )

                st.markdown(
                    f"""
                    <div style="
                        color:#5548E8;
                        font-size:23px;
                        font-weight:800;
                        margin:8px 0;
                    ">
                        ₹{product['subtotal']:,.2f}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.caption(
                    f"Quantity: {product['quantity']} · "
                    f"Available stock: {product['stock']}"
                )

            with col2:

                new_quantity = st.number_input(
                    "Quantity",
                    min_value=1,
                    max_value=max(1, product["stock"]),
                    value=min(
                        product["quantity"],
                        max(1, product["stock"]),
                    ),
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

    # -----------------------------------------
    # ORDER SUMMARY
    # -----------------------------------------

    st.divider()

    st.markdown("## 💰 Order Summary")

    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:
            st.write("Total Product Types")

        with col2:
            st.write(f"**{len(cart_items)}**")

        col1, col2 = st.columns(2)

        with col1:
            st.write("Total Items")

        with col2:
            st.write(f"**{total_items}**")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Total Amount")

        with col2:
            st.markdown(
                f"""
                <div style="
                    color:#5548E8;
                    font-size:25px;
                    font-weight:800;
                    text-align:right;
                ">
                    ₹{total_price:,.2f}
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.caption(
        "Prices are based on the ShopMind product catalogue. "
        "Taxes, shipping, and payment processing are not included."
    )

    # -----------------------------------------
    # CHECKOUT
    # -----------------------------------------

    st.divider()

    st.markdown("## 📦 Complete Your Order")

    if st.button(
        "🛒 Place Order",
        use_container_width=True,
        type="primary",
    ):

        success, result = place_order(user_id)

        if success:

            st.session_state["order_confirmation"] = result

            st.rerun()

        else:

            st.error(result)

    # -----------------------------------------
    # CLEAR CART
    # -----------------------------------------

    st.divider()

    if st.button(
        "🗑️ Clear Entire Cart",
        use_container_width=True,
    ):

        clear_cart(user_id)

        st.success("Your cart has been cleared!")

        st.rerun()