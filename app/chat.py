import streamlit as st
from database.wishlist import add_to_wishlist
from database.cart import add_to_cart


def render_product_cards(products):

    if not products:
        return

    st.markdown("### 🛍️ Recommended Products")

    columns = st.columns(2)

    current_user = st.session_state.get("current_user")

    for index, product in enumerate(products):

        with columns[index % 2]:

            with st.container(border=True):

                # Product name
                st.markdown(
                    f"""
                    <div style="
                        color: #6C63FF;
                        font-size: 12px;
                        font-weight: 700;
                        letter-spacing: 1px;
                        text-transform: uppercase;
                    ">
                        {product.get('category', 'Product')}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown(f"### {product['name']}")

                st.caption(f"Brand: {product.get('brand', 'N/A')}")

                # Price and rating
                price_col, rating_col = st.columns(2)

                with price_col:
                    st.markdown(
                        f"""
                        <div style="
                            font-size: 25px;
                            font-weight: 800;
                            color: #5548E8;
                            padding: 5px 0;
                        ">
                            ₹{product['price']:,.0f}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with rating_col:
                    st.metric(
                        "Rating",
                        f"⭐ {product.get('rating', 0)}/5",
                    )

                # Description
                description = product.get(
                    "description",
                    "No description available."
                )

                st.write(description)

                # Stock indicator
                stock = product.get("stock", 0)

                if stock > 5:
                    st.success(f"● In Stock ({stock} available)")
                elif stock > 0:
                    st.warning(f"● Only {stock} left")
                else:
                    st.error("● Out of Stock")

                # Customer actions
                if current_user:

                    st.divider()

                    if st.button(
                        "❤️ Add to Wishlist",
                        key=f"chat_wishlist_{product['id']}",
                        use_container_width=True,
                    ):

                        success, message = add_to_wishlist(
                            current_user["id"],
                            product["id"],
                        )

                        if success:
                            st.success(message)
                        else:
                            st.info(message)

                    if stock > 0:

                        quantity = st.number_input(
                            "Quantity",
                            min_value=1,
                            max_value=max(1, stock),
                            value=1,
                            key=f"chat_cart_quantity_{product['id']}",
                        )

                        if st.button(
                            "🛒 Add to Cart",
                            key=f"chat_cart_{product['id']}",
                            use_container_width=True,
                        ):

                            success, message = add_to_cart(
                                current_user["id"],
                                product["id"],
                                quantity,
                            )

                            if success:
                                st.success(message)
                            else:
                                st.warning(message)


def render_chat_history():

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if message["role"] == "assistant":

                render_product_cards(
                    message.get("products", [])
                )


def process_chat_request(shopmind, user_input, category, budget):

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner("ShopMind is finding the best products..."):

            try:

                result = shopmind.process_request_data(
                    message=user_input,
                    category_override=(
                        category
                        if category != "All Categories"
                        else None
                    ),
                    budget_override=(
                        budget
                        if budget < 150000
                        else None
                    )
                )

                response = result.get("response", "")

                if isinstance(response, dict):
                    response = shopmind.comparison_agent.format_comparison(
                        response
                    )

                products = result.get("products", [])

                st.markdown(response)

                render_product_cards(products)

                # Save shopping history
                from database.history import record_search

                current_user = st.session_state.get("current_user")

                record_search(
                    query=user_input,
                    category=(
                        category
                        if category != "All Categories"
                        else None
                    ),
                    budget=budget if budget < 150000 else None,
                    products=products,
                    user_id=(
                        str(current_user["id"])
                        if current_user
                        else "guest"
                    )
                )

            except Exception as error:

                print("ShopMind Error:", error)

                response = (
                    "Something went wrong while processing your request. "
                    "Please try again."
                )

                products = []

                st.error(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "products": products
    })


def render_chat(shopmind, category="All Categories", budget=150000):

    if "messages" not in st.session_state:
        st.session_state.messages = []

    render_chat_history()

    user_input = st.chat_input(
        "Ask ShopMind to find your perfect product..."
    )

    if st.session_state.get("pending_prompt"):

        user_input = st.session_state.pending_prompt
        st.session_state.pending_prompt = None

    if user_input:

        process_chat_request(
            shopmind,
            user_input,
            category,
            budget
        )
