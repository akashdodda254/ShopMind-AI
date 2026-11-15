import streamlit as st

from database.db import get_all_products
from price_tracker.tracker import PriceTracker


def render_price_dashboard():

    st.markdown("# 📉 Price Intelligence")

    st.caption(
        "Track catalogue prices, monitor price changes, "
        "and understand historical pricing."
    )

    products = get_all_products()

    if not products:
        st.info("No products available.")
        return

    tracker = PriceTracker()
    tracker.create_table()

    product_options = {
        f"{product['name']} — ₹{product['price']:,.0f}": product
        for product in products
    }

    selected_name = st.selectbox(
        "🔎 Select a product",
        list(product_options.keys()),
    )

    selected_product = product_options[selected_name]

    product_id = selected_product["id"]
    current_price = selected_product["price"]

    # PRODUCT OVERVIEW

    st.divider()

    st.markdown("## Product Price Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Current Catalogue Price",
            f"₹{current_price:,.2f}",
        )

    with col2:
        st.metric(
            "Product Rating",
            f"⭐ {selected_product['rating']}/5",
        )

    with col3:
        st.metric(
            "Review Count",
            f"{selected_product['rating_count']:,}",
        )

    st.info(
        "This price comes from your ShopMind catalogue. "
        "It is not a live retailer price."
    )

    # PRICE ACTIONS

    st.markdown("## ⚡ Price Monitoring")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.markdown("### 📌 Record Price")

            st.write(
                "Save the current catalogue price "
                "to your product's price history."
            )

            if st.button(
                "Record Current Price",
                use_container_width=True,
            ):

                tracker.record_price(
                    product_id,
                    current_price,
                )

                st.success("Price recorded successfully!")

    with col2:

        with st.container(border=True):

            st.markdown("### 🔔 Price Drop Detection")

            st.write(
                "Check whether the current price "
                "has dropped compared with previous records."
            )

            if st.button(
                "Check Price Drop",
                use_container_width=True,
            ):

                result = tracker.check_price_drop(
                    product_id,
                    current_price,
                )

                if result:
                    st.success(f"Price drop detected: {result}")
                else:
                    st.info("No price drop detected.")

    # PRICE HISTORY

    st.divider()

    st.markdown("## 📊 Historical Price Records")

    history = tracker.get_price_history(product_id)

    if history:

        st.caption(
            f"{len(history)} historical price record(s) available."
        )

        for index, entry in enumerate(history, start=1):

            with st.container(border=True):

                st.markdown(f"**Price Record {index}**")
                st.write(entry)

    else:

        st.info(
            "No price history available yet. "
            "Record the current price to start tracking."
        )