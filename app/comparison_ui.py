import streamlit as st

from database.db import get_all_products
from agents.comparison_agent import ComparisonAgent


def render_comparison():

    st.markdown("# ⚖️ Product Comparison")

    st.caption(
        "Compare products side by side and discover which one "
        "offers the best value for your needs."
    )

    products = get_all_products()

    if not products:
        st.info("No products available for comparison.")
        return

    product_options = {
        product["name"]: product
        for product in products
    }

    selected_names = st.multiselect(
        "🔎 Select products to compare",
        list(product_options.keys()),
        max_selections=4,
        placeholder="Choose at least two products...",
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

    # -----------------------------------------
    # PRODUCT COMPARISON CARDS
    # -----------------------------------------

    st.divider()

    st.markdown("## 📊 Side-by-Side Comparison")

    columns = st.columns(len(selected_products))

    for index, product in enumerate(selected_products):

        with columns[index]:

            with st.container(border=True):

                st.markdown(
                    """
                    <div style="
                        background: #F0EDFF;
                        color: #5548E8;
                        display: inline-block;
                        padding: 5px 10px;
                        border-radius: 20px;
                        font-size: 11px;
                        font-weight: 700;
                    ">
                        PRODUCT COMPARISON
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
                        font-size: 28px;
                        font-weight: 800;
                        color: #5548E8;
                        margin: 12px 0;
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

                st.write(
                    f"📝 Reviews: {product['rating_count']:,}"
                )

                stock = product.get("stock", 0)

                if stock > 5:
                    st.success(f"In Stock ({stock})")
                elif stock > 0:
                    st.warning(f"Only {stock} left")
                else:
                    st.error("Out of Stock")

                st.divider()

                st.markdown("**Specifications**")

                specifications = product.get(
                    "specifications",
                    "Specifications unavailable.",
                )

                st.write(specifications)

    # -----------------------------------------
    # COMPARISON INSIGHTS
    # -----------------------------------------

    st.divider()

    st.markdown("## 🏆 Comparison Insights")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.caption("💰 CHEAPEST PRODUCT")
            st.markdown(
                f"### {comparison['cheapest']['name']}"
            )

    with col2:
        with st.container(border=True):
            st.caption("⭐ HIGHEST RATED")
            st.markdown(
                f"### {comparison['highest_rated']['name']}"
            )

    with col3:
        with st.container(border=True):
            st.caption("🔥 MOST REVIEWED")
            st.markdown(
                f"### {comparison['most_popular']['name']}"
            )

    st.metric(
        "Overall Price Difference",
        f"₹{comparison['price_difference']:,.0f}",
    )

    # -----------------------------------------
    # AI COMPARISON ANALYSIS
    # -----------------------------------------

    st.divider()

    st.markdown("## 🤖 AI Comparison Analysis")

    st.write(
        "Let ShopMind analyze the selected products and "
        "help you understand their strengths and differences."
    )

    if st.button(
        "✨ Analyze Products with Gemini",
        use_container_width=True,
    ):

        with st.spinner("ShopMind is analyzing your products..."):

            try:

                analysis = comparison_agent.generate_ai_analysis(
                    comparison
                )

                st.session_state["comparison_analysis"] = analysis

            except Exception as error:

                st.error(
                    "Unable to generate AI analysis. Please try again."
                )

                print("Comparison Analysis Error:", error)

    analysis = st.session_state.get("comparison_analysis")

    if analysis:

        with st.container(border=True):

            st.markdown("### 💡 ShopMind's Recommendation")

            st.write(analysis)