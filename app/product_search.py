import streamlit as st

from database.product_search import (
    advanced_search_products,
    get_product_filter_options
)

from database.wishlist import add_to_wishlist
from database.cart import add_to_cart


def render_advanced_search():

    st.title("🔎 Advanced Product Search")

    st.caption(
        "Find exactly what you're looking for using "
        "powerful shopping filters."
    )

    # Load available filters
    filter_options = get_product_filter_options()

    categories = ["All Categories"] + filter_options["categories"]
    brands = ["All Brands"] + filter_options["brands"]

    # Search keyword
    keyword = st.text_input(
        "Search products",
        placeholder="Search laptops, Samsung, gaming, 16GB RAM..."
    )

    st.markdown("### Refine Your Search")

    col1, col2 = st.columns(2)

    with col1:

        category = st.selectbox(
            "Category",
            categories
        )

        brand = st.selectbox(
            "Brand",
            brands
        )

        min_rating = st.selectbox(
            "Minimum Rating",
            [0, 3, 3.5, 4, 4.5]
        )

    with col2:

        min_price = st.number_input(
            "Minimum Price (₹)",
            min_value=0,
            value=0,
            step=1000
        )

        max_price = st.number_input(
            "Maximum Price (₹)",
            min_value=0,
            value=150000,
            step=1000
        )

        sort_options = {
            "Most Relevant": "relevance",
            "Price: Low to High": "price_low",
            "Price: High to Low": "price_high",
            "Highest Rated": "rating",
            "Most Popular": "popularity",
            "Newest": "newest"
        }

        sort_label = st.selectbox(
            "Sort By",
            list(sort_options.keys())
        )

    in_stock_only = st.checkbox(
        "Show only products currently in stock"
    )

    # Search button
    if st.button(
        "🔍 Search Products",
        use_container_width=True
    ):

        try:

            products = advanced_search_products(
                keyword=keyword,
                category=(
                    None if category == "All Categories"
                    else category
                ),
                brand=(
                    None if brand == "All Brands"
                    else brand
                ),
                min_price=min_price if min_price > 0 else None,
                max_price=max_price,
                min_rating=min_rating if min_rating > 0 else None,
                sort_by=sort_options[sort_label],
                in_stock_only=in_stock_only
            )

            st.session_state.advanced_search_results = products
            st.session_state.advanced_search_performed = True

        except ValueError as error:

            st.error(str(error))
            return

    # Display results
    if st.session_state.get("advanced_search_performed"):

        products = st.session_state.get(
            "advanced_search_results",
            []
        )

        st.divider()

        st.subheader(
            f"Search Results ({len(products)})"
        )

        if not products:

            st.info(
                "No products found. Try changing your search filters."
            )

            return

        current_user = st.session_state.get("current_user")

        columns = st.columns(2)

        for index, product in enumerate(products):

            with columns[index % 2]:

                with st.container(border=True):

                    st.caption(
                        f"{product['category']} · {product['brand']}"
                    )

                    if st.button(
                        "View Product Details",
                        key=f"view_details_{product['id']}",
                        use_container_width=True
                    ):
                        st.session_state.selected_product_id = product["id"]
                        st.session_state.pending_page = "Product Details"
                        st.rerun()

                    st.markdown(
                        f"**₹{product['price']:,.0f}**"
                    )

                    st.write(
                        f"⭐ {product['rating']}/5 "
                        f"({product['rating_count']} ratings)"
                    )

                    st.write(product.get("description", ""))

                    st.caption(
                        f"Specifications: "
                        f"{product.get('specifications', 'N/A')}"
                    )

                    if product["stock"] > 0:

                        st.success(
                            f"In Stock: {product['stock']}"
                        )

                    else:

                        st.error("Out of Stock")

                    if current_user:

                        if st.button(
                            "❤️ Add to Wishlist",
                            key=f"search_wishlist_{product['id']}",
                            use_container_width=True
                        ):

                            success, message = add_to_wishlist(
                                current_user["id"],
                                product["id"]
                            )

                            if success:
                                st.success(message)
                            else:
                                st.info(message)

                        if product["stock"] > 0:

                            quantity = st.number_input(
                                "Quantity",
                                min_value=1,
                                max_value=product["stock"],
                                value=1,
                                key=f"search_quantity_{product['id']}"
                            )

                            if st.button(
                                "🛒 Add to Cart",
                                key=f"search_cart_{product['id']}",
                                use_container_width=True
                            ):

                                success, message = add_to_cart(
                                    current_user["id"],
                                    product["id"],
                                    quantity
                                )

                                if success:
                                    st.success(message)
                                else:
                                    st.warning(message)