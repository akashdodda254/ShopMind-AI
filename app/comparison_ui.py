import streamlit as st

from database.db import get_all_products
from agents.comparison_agent import ComparisonAgent


def render_comparison():

    st.subheader("⚖️ Product Comparison")

    products = get_all_products()

    if not products:
        st.info("No products available for comparison.")
        return

    product_options = {
        product["name"]: product
        for product in products
    }

    selected_names = st.multiselect(
        "Select products to compare",
        list(product_options.keys()),
        max_selections=4
    )

    if len(selected_names) < 2:
        st.info("Select at least two products to compare.")
        return

    selected_products = [
        product_options[name]
        for name in selected_names
    ]

    comparison_agent = ComparisonAgent()

    comparison = comparison_agent.compare(selected_products)

    if not comparison:
        st.warning("Unable to compare these products.")
        return

    st.divider()
    st.subheader("📊 Comparison Results")

    columns = st.columns(len(selected_products))

    for index, product in enumerate(selected_products):

        with columns[index]:

            st.markdown(f"### {product['name']}")

            st.markdown(
                f"### ₹{product['price']:,.0f}"
            )

            st.write(f"Brand: {product['brand']}")

            st.write(f"Rating: ⭐ {product['rating']}/5")

            st.write(
                f"Reviews: {product['rating_count']}"
            )

            st.write(f"Stock: {product['stock']}")

            st.caption(product["specifications"])

    st.divider()

    st.subheader("🏆 Comparison Insights")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Cheapest Product",
        comparison["cheapest"]["name"]
    )

    col2.metric(
        "Highest Rated",
        comparison["highest_rated"]["name"]
    )

    col3.metric(
        "Most Reviewed",
        comparison["most_popular"]["name"]
    )

    st.metric(
        "Price Difference",
        f"₹{comparison['price_difference']:,.0f}"
    )

    if st.button("🤖 Analyze with Gemini"):

        with st.spinner("Analyzing products..."):

            analysis = comparison_agent.generate_ai_analysis(
                comparison
            )

            st.session_state["comparison_analysis"] = analysis

    analysis = st.session_state.get("comparison_analysis")

    if analysis:
        st.divider()
        st.subheader("🤖 AI Comparison Analysis")
        st.write(analysis)