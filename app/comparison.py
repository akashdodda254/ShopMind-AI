import streamlit as st

from database.db import get_all_products
from agents.comparison_agent import ComparisonAgent


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ShopMind Product Comparison",
    page_icon="⚖️",
    layout="wide"
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("⚖️ ShopMind Product Comparison")

st.caption(
    "Compare products, analyze specifications "
    "and discover the best value for money."
)

st.divider()


# --------------------------------------------------
# LOAD PRODUCTS
# --------------------------------------------------

products = get_all_products()


if not products:

    st.warning("No products available in the database.")

else:

    product_names = [
        product["name"] for product in products
    ]


    # --------------------------------------------------
    # PRODUCT SELECTION
    # --------------------------------------------------

    st.subheader("Select Products")

    selected_names = st.multiselect(
        "Choose at least two products to compare",
        product_names,
        max_selections=4
    )


    if len(selected_names) >= 2:

        selected_products = [
            product for product in products
            if product["name"] in selected_names
        ]

        comparison_agent = ComparisonAgent()

        result = comparison_agent.compare(
            selected_products
        )


        # --------------------------------------------------
        # SIDE-BY-SIDE COMPARISON
        # --------------------------------------------------

        st.divider()

        st.subheader("📊 Product Comparison")

        columns = st.columns(len(selected_products))

        for index, product in enumerate(selected_products):

            with columns[index]:

                st.markdown(f"### {product['name']}")

                st.metric(
                    "Price",
                    f"₹{product['price']:,.0f}"
                )

                st.metric(
                    "Rating",
                    f"⭐ {product['rating']}/5"
                )

                st.write(f"**Brand:** {product['brand']}")

                st.write(
                    f"**Reviews:** {product['rating_count']:,}"
                )

                st.write(
                    f"**Available Stock:** {product['stock']}"
                )

                st.markdown("**Specifications**")

                st.info(
                    product.get("specifications") or "Not available"
                )


        # --------------------------------------------------
        # COMPARISON INSIGHTS
        # --------------------------------------------------

        st.divider()

        st.subheader("🏆 Shopping Insights")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.success(
                f"**Lowest Price**\n\n"
                f"{result['cheapest']['name']}\n\n"
                f"₹{result['cheapest']['price']:,.0f}"
            )

        with col2:

            st.info(
                f"**Highest Rating**\n\n"
                f"{result['highest_rated']['name']}\n\n"
                f"{result['highest_rated']['rating']}/5"
            )

        with col3:

            st.warning(
                f"**Most Reviewed**\n\n"
                f"{result['most_popular']['name']}\n\n"
                f"{result['most_popular']['rating_count']:,} reviews"
            )

        st.metric(
            "Price Difference",
            f"₹{result['price_difference']:,.0f}"
        )


        # --------------------------------------------------
        # SPECIFICATION COMPARISON
        # --------------------------------------------------

        st.divider()

        st.subheader("🔍 Specification Comparison")

        specifications = comparison_agent.compare_specifications(
            selected_products
        )

        all_keys = sorted({
            key
            for product_specs in specifications.values()
            for key in product_specs
        })

        if all_keys:

            comparison_data = {
                "Specification": all_keys
            }

            for product_name, product_specs in specifications.items():

                comparison_data[product_name] = [
                    product_specs.get(key, "Not available")
                    for key in all_keys
                ]

            st.dataframe(
                comparison_data,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No structured specifications available.")


        # --------------------------------------------------
        # GEMINI AI ANALYSIS
        # --------------------------------------------------

        st.divider()

        st.subheader("🤖 ShopMind AI Analysis")

        if st.button(
            "Analyze Products with Gemini",
            use_container_width=True
        ):

            with st.spinner(
                "Gemini is analyzing your selected products..."
            ):

                try:

                    analysis = (
                        comparison_agent.generate_ai_analysis(
                            result
                        )
                    )

                    st.session_state.comparison_analysis = analysis

                except Exception as error:

                    print("Gemini comparison error:", error)

                    st.error(
                        "Unable to generate AI analysis. "
                        "Please try again."
                    )

        if "comparison_analysis" in st.session_state:

            st.markdown(
                st.session_state.comparison_analysis
            )


    else:

        st.info(
            "👆 Select at least two products to start comparing."
        )