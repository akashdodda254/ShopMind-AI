import streamlit as st
import pandas as pd

from database.admin import (
    is_admin,
    get_dashboard_stats,
    get_all_users,
    get_all_orders,
    admin_update_order_status,
    get_inventory,
)


def render_admin_dashboard():

    st.markdown("# 🛡️ ShopMind Administration")

    st.caption(
        "Manage users, monitor orders, and oversee your shopping platform."
    )

    current_user = st.session_state.get("current_user")

    if not current_user:
        st.warning("Please log in first.")
        return

    admin_id = current_user["id"]

    # -----------------------------------------
    # ADMIN ACCESS CONTROL
    # -----------------------------------------

    if not is_admin(admin_id):
        st.error(
            "Access denied. Administrator privileges required."
        )
        return

    # -----------------------------------------
    # ADMIN HEADER
    # -----------------------------------------

    st.markdown(
        """
        <div style="
            background: linear-gradient(120deg, #171A2E, #5548E8, #8177FF);
            padding: 28px;
            border-radius: 18px;
            margin: 15px 0 25px 0;
        ">
            <div style="
                color:rgba(255,255,255,0.75);
                font-size:12px;
                font-weight:700;
                letter-spacing:2px;
            ">
                ADMIN CONTROL CENTER
            </div>

            <h2 style="color:white; margin:8px 0;">
                Welcome to ShopMind Admin 🚀
            </h2>

            <p style="color:rgba(255,255,255,0.85); margin:0;">
                Your central workspace for managing ShopMind.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------
    # BUSINESS STATISTICS
    # -----------------------------------------

    stats = get_dashboard_stats(admin_id)

    st.markdown("## 📊 Business Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "👥 Registered Users",
            stats["total_users"],
        )

    with col2:
        st.metric(
            "🛍️ Total Products",
            stats["total_products"],
        )

    with col3:
        st.metric(
            "📦 Total Orders",
            stats["total_orders"],
        )

    col4, col5 = st.columns(2)

    with col4:
        st.metric(
            "💰 Order Value",
            f"₹{stats['total_revenue']:,.2f}",
        )

    with col5:
        st.metric(
            "⏳ Pending Orders",
            stats["pending_orders"],
        )

    st.info(
        "Order value represents the total value of non-cancelled "
        "orders. It is not verified payment revenue."
    )

    st.divider()

    # -----------------------------------------
    # ADMIN NAVIGATION
    # -----------------------------------------

    st.markdown("## ⚙️ Administration")

    admin_section = st.radio(
        "Choose administration section",
        [
            "Overview",
            "User Management",
            "Order Management",
            "Inventory Management",
        ],
        horizontal=True,
        label_visibility="collapsed",
    )

    st.divider()

    # -----------------------------------------
    # OVERVIEW
    # -----------------------------------------

    if admin_section == "Overview":

        st.markdown("## 📈 Platform Overview")

        col1, col2 = st.columns(2)

        with col1:

            with st.container(border=True):

                st.markdown("### 👥 User Activity")

                st.metric(
                    "Registered Users",
                    stats["total_users"],
                )

        with col2:

            with st.container(border=True):

                st.markdown("### 📦 Order Activity")

                st.metric(
                    "Total Orders",
                    stats["total_orders"],
                )

        st.success(
            "ShopMind administration panel is ready."
        )

    # -----------------------------------------
    # USER MANAGEMENT
    # -----------------------------------------

    elif admin_section == "User Management":

        st.markdown("## 👥 User Management")

        users = get_all_users(admin_id)

        if users:

            users_df = pd.DataFrame(users)

            st.caption(
                f"{len(users)} registered user(s)"
            )

            st.dataframe(
                users_df,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info("No registered users found.")

    # -----------------------------------------
    # ORDER MANAGEMENT
    # -----------------------------------------

    elif admin_section == "Order Management":

        st.markdown("## 📦 Order Management")

        orders = get_all_orders(admin_id)

        if not orders:

            st.info("No orders found.")

        else:

            orders_df = pd.DataFrame(orders)

            st.dataframe(
                orders_df,
                use_container_width=True,
                hide_index=True,
            )

            st.divider()

            st.markdown("### Update Customer Order")

            order_options = {
                f"Order #{order['id']} — {order['username']}": order
                for order in orders
            }

            selected_order_name = st.selectbox(
                "Select an order",
                list(order_options.keys()),
            )

            selected_order = order_options[selected_order_name]

            statuses = [
                "Placed",
                "Processing",
                "Shipped",
                "Delivered",
                "Cancelled",
            ]

            new_status = st.selectbox(
                "Update Order Status",
                statuses,
                index=statuses.index(
                    selected_order["status"]
                ),
            )

            if st.button(
                "💾 Update Order",
                use_container_width=True,
                type="primary",
            ):

                success, message = admin_update_order_status(
                    admin_id,
                    selected_order["id"],
                    new_status,
                )

                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

    # -----------------------------------------
    # INVENTORY MANAGEMENT
    # -----------------------------------------

    elif admin_section == "Inventory Management":

        st.markdown("## 📦 Inventory Management")

        products = get_inventory(admin_id)

        if products:

            inventory_df = pd.DataFrame(products)

            total_products = len(products)

            low_stock = [
                product
                for product in products
                if product["stock"] <= 5
            ]

            out_of_stock = [
                product
                for product in products
                if product["stock"] == 0
            ]

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Total Products",
                    total_products,
                )

            with col2:
                st.metric(
                    "Low Stock",
                    len(low_stock),
                )

            with col3:
                st.metric(
                    "Out of Stock",
                    len(out_of_stock),
                )

            st.divider()

            st.markdown("### 📋 Product Inventory")

            st.dataframe(
                inventory_df,
                use_container_width=True,
                hide_index=True,
            )

            st.divider()

            st.markdown("### ⚠️ Inventory Alerts")

            if low_stock:

                st.warning(
                    f"{len(low_stock)} product(s) have "
                    "5 or fewer units remaining."
                )

                for product in low_stock:

                    if product["stock"] == 0:
                        st.error(
                            f"{product['name']} — Out of stock"
                        )
                    else:
                        st.warning(
                            f"{product['name']} — "
                            f"{product['stock']} units remaining"
                        )

            else:

                st.success(
                    "No low-stock products detected."
                )

        else:

            st.info("No inventory records found.")