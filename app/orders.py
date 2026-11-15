import streamlit as st

from database.orders import (
    get_user_orders,
    get_order_details,
    cancel_order,
)


def render_orders():

    st.markdown("# 📦 My Orders")

    st.caption(
        "Track your purchases and manage your ShopMind orders."
    )

    current_user = st.session_state.get("current_user")

    if not current_user:
        st.warning("Please log in to view your orders.")
        return

    user_id = current_user["id"]

    orders = get_user_orders(user_id)

    # -----------------------------------------
    # ORDER SUMMARY
    # -----------------------------------------

    total_orders = len(orders)

    total_spent = sum(
        order["total_amount"]
        for order in orders
        if order["status"] != "Cancelled"
    )

    active_orders = sum(
        1 for order in orders
        if order["status"] not in ["Delivered", "Cancelled"]
    )

    # -----------------------------------------
    # PAGE HEADER
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
                Your Shopping Journey 💜
            </h2>
            <p style="color:rgba(255,255,255,0.9); margin:8px 0 0 0;">
                Every purchase, organized in one place.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📦 Total Orders", total_orders)

    with col2:
        st.metric("💰 Purchase Value", f"₹{total_spent:,.2f}")

    with col3:
        st.metric("🚚 Active Orders", active_orders)

    st.divider()

    # -----------------------------------------
    # EMPTY ORDER HISTORY
    # -----------------------------------------

    if not orders:

        with st.container(border=True):

            st.markdown(
                """
                <div style="
                    text-align:center;
                    padding:35px 15px;
                ">
                    <div style="font-size:55px;">📦</div>
                    <h2 style="color:#5548E8;">
                        No Orders Yet
                    </h2>
                    <p style="color:#7B8298;">
                        Your purchase history will appear here
                        when you place your first order.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        return

    # -----------------------------------------
    # ORDER HISTORY
    # -----------------------------------------

    st.markdown("## 📋 Your Order History")

    for order in orders:

        order_id = order["id"]
        status = order["status"]

        with st.container(border=True):

            col1, col2 = st.columns([3, 1])

            with col1:

                st.markdown(f"### Order #{order_id}")

                st.caption(
                    f"📅 Ordered on: {order['created_at']}"
                )

                st.markdown(
                    f"""
                    <div style="
                        color:#5548E8;
                        font-size:23px;
                        font-weight:800;
                        margin:8px 0;
                    ">
                        ₹{order['total_amount']:,.2f}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col2:

                st.caption("ORDER STATUS")

                if status == "Delivered":
                    st.success(f"✓ {status}")

                elif status == "Cancelled":
                    st.error(f"✕ {status}")

                elif status == "Shipped":
                    st.info(f"🚚 {status}")

                elif status == "Processing":
                    st.info(f"⏳ {status}")

                else:
                    st.warning(f"● {status}")

            # ---------------------------------
            # PURCHASED PRODUCTS
            # ---------------------------------

            with st.expander("📦 View Purchased Products"):

                details = get_order_details(
                    order_id,
                    user_id,
                )

                if details:

                    for item in details["items"]:

                        st.markdown(
                            f"### {item['product_name']}"
                        )

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.caption("QUANTITY")
                            st.write(item["quantity"])

                        with col2:
                            st.caption("UNIT PRICE")
                            st.write(
                                f"₹{item['unit_price']:,.2f}"
                            )

                        with col3:
                            st.caption("SUBTOTAL")
                            st.write(
                                f"₹{item['subtotal']:,.2f}"
                            )

                        st.divider()

                else:

                    st.info("No product details available.")

            # ---------------------------------
            # ORDER CANCELLATION
            # ---------------------------------

            if status == "Placed":

                if st.button(
                    "❌ Cancel Order",
                    key=f"cancel_order_{order_id}",
                    use_container_width=True,
                ):

                    success, message = cancel_order(
                        order_id,
                        user_id,
                    )

                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)