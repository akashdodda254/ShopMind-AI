import streamlit as st

from database.db import get_all_products
from price_tracker.tracker import PriceTracker


def render_price_dashboard():

    st.subheader("📉 Product Price Tracker")

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
        "Select a product",
        list(product_options.keys()),
    )

    selected_product = product_options[selected_name]

    product_id = selected_product["id"]
    current_price = selected_product["price"]

    st.metric(
        "Current Catalogue Price",
        f"₹{current_price:,.2f}",
    )

    st.caption(
        "This is the price stored in your ShopMind catalogue, "
        "not a live retailer price."
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📌 Record Current Price", use_container_width=True):
            tracker.record_price(product_id, current_price)
            st.success("Price recorded successfully!")

    with col2:
        if st.button("🔔 Check Price Drop", use_container_width=True):
            result = tracker.check_price_drop(product_id, current_price)

            if result:
                st.success(f"Price drop detected: {result}")
            else:
                st.info("No price drop detected.")

    st.divider()

    st.subheader("📊 Price History")

    history = tracker.get_price_history(product_id)

    if history:
        for entry in history:
            st.write(entry)
    else:
        st.info("No price history available. Record a price to get started.")