from recommendation.personalized_engine import PersonalizedRecommendationEngine
from reviews.review_sentiment import ReviewSentimentAnalyzer
import streamlit as st

from agents.orchestrator import ShopMindOrchestrator

from database.history import (
    record_search,
    get_recent_searches,
    learn_preferences
)
from reviews.review_analyzer import ReviewAnalyzer

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="ShopMind AI",
    page_icon="🛍️",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
}

.shop-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0;
}

.shop-subtitle {
    color: #a0a0a0;
    font-size: 16px;
    margin-top: 5px;
}

.product-card {
    background-color: #1e222d;
    border: 1px solid #343a46;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 15px;
}

.product-name {
    font-size: 19px;
    font-weight: 700;
    margin-bottom: 8px;
}

.product-price {
    font-size: 25px;
    font-weight: 800;
    color: #55d6a0;
}

.product-info {
    color: #b5b5b5;
    font-size: 14px;
    margin-top: 8px;
}

.section-title {
    font-size: 24px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# INITIALIZE SHOPMIND
# --------------------------------------------------

@st.cache_resource
def initialize_shopmind():
    return ShopMindOrchestrator()


shopmind = initialize_shopmind()


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


# --------------------------------------------------
# HEADER
# --------------------------------------------------

header_left, header_right = st.columns([4, 1])

with header_left:

    st.markdown(
        '<p class="shop-title">🛍️ ShopMind AI</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="shop-subtitle">'
        'Your intelligent personal shopping assistant'
        '</p>',
        unsafe_allow_html=True
    )

with header_right:

    st.markdown("### 🟢 AI Online")


st.divider()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------


with st.sidebar:

    st.title("🛍️ ShopMind")
    st.caption("Smart shopping starts here.")

    st.divider()

    # SHOPPING FILTERS
    st.subheader("Shopping Filters")

    category = st.selectbox(
        "Product Category",
        [
            "All Categories",
            "Laptop",
            "Smartphone",
            "Headphones",
            "Smartwatch"
        ]
    )

    budget = st.slider(
        "Maximum Budget (₹)",
        min_value=5000,
        max_value=150000,
        value=150000,
        step=5000
    )

    st.caption(f"Maximum budget: ₹{budget:,}")

    st.divider()

    # PERSONALIZED PREFERENCES
    st.subheader("❤️ Your Preferences")

    preferred_categories = st.multiselect(
        "Preferred Categories",
        ["Laptops", "Smartphones", "Headphones", "Smartwatches"]
    )

    preferred_brands = st.multiselect(
        "Preferred Brands",
        [
            "ASUS",
            "Apple",
            "Samsung",
            "HP",
            "Acer",
            "Sony",
            "Bose",
            "OnePlus"
        ]
    )

    preferred_budget = st.number_input(
        "Personal Budget (₹)",
        min_value=1000,
        max_value=200000,
        value=75000,
        step=5000
    )

    preferred_rating = st.slider(
        "Minimum Product Rating",
        min_value=0.0,
        max_value=5.0,
        value=4.0,
        step=0.1
    )

    if st.button(
        "🎯 Get Personalized Recommendations",
        use_container_width=True
    ):

        engine = PersonalizedRecommendationEngine()

        learned = learn_preferences()

        preferences = {
            "categories": list(set(preferred_categories + learned["categories"])),
            "brands": preferred_brands,
            "keywords": learned["keywords"],
            "max_budget": preferred_budget,
            "min_rating": preferred_rating
        }

        recommendations = engine.recommend(preferences)

        st.session_state["personalized_recommendations"] = recommendations

    st.divider()

    # QUICK SEARCHES
    st.subheader("⚡ Quick Searches")

    suggestions = [
        "Find gaming laptops",
        "Recommend smartphones",
        "Find headphones",
        "Compare laptops"
    ]

    for suggestion in suggestions:

        if st.button(suggestion, use_container_width=True):
            st.session_state.pending_prompt = suggestion

    st.divider()

    # SHOPPING HISTORY
    st.subheader("🕒 Recent Shopping History")

    recent_searches = get_recent_searches(limit=5)

    if recent_searches:

        for search in recent_searches:
            st.caption(f"🔍 {search['query']}")
            st.caption(f"Date: {search['created_at']}")

    else:
        st.caption("No shopping history yet.")
        st.divider()

    st.divider()

    # REVIEW ANALYSIS
    st.subheader("⭐ Product Review Analysis")

    if st.button("Analyze Product Ratings", use_container_width=True):
        analyzer = ReviewAnalyzer()

        st.session_state["review_analysis"] = (
            analyzer.analyze_all_products()
        )
    st.divider()    
    # CLEAR CHAT
    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.session_state.pop("personalized_recommendations", None)

        st.rerun()


# --------------------------------------------------
# PERSONALIZED RECOMMENDATIONS (MAIN PAGE)
# --------------------------------------------------

if "personalized_recommendations" in st.session_state:
    st.markdown("### 🎯 Your Personalized Recommendations")
    recommendations = st.session_state["personalized_recommendations"]

    if not recommendations:
        st.info("No products match your preferences. Try increasing your budget or lowering the minimum rating.")
    else:
        recommendation_columns = st.columns(2)
        for index, item in enumerate(recommendations):
            product = item["product"]
            with recommendation_columns[index % 2]:
                with st.container(border=True):
                    st.markdown(f"#### {product['name']}")
                    st.markdown(f"**₹{product['price']:,.0f}**")
                    st.write(f"⭐ {product['rating']}/5 · {product['rating_count']} reviews")
                    st.caption(f"Brand: {product['brand']} | Stock: {product['stock']}")
                    st.caption(f"Specifications: {product['specifications']}")
                    st.caption(f"Match score: {item['score']:.2f}")

    st.divider()
    
# CUSTOMER SENTIMENT ANALYSIS

st.divider()
st.subheader("💬 Customer Review Sentiment Analysis")

review_text = st.text_area(
    "Enter customer reviews (one review per line)",
    placeholder="Battery life is excellent!\nThe product is too expensive.\nGood performance for the price."
)

if st.button("Analyze Customer Sentiment"):

    reviews = [
        review.strip()
        for review in review_text.splitlines()
        if review.strip()
    ]

    if reviews:

        analyzer = ReviewSentimentAnalyzer()

        with st.spinner("Gemini is analyzing customer reviews..."):

            results = analyzer.analyze_reviews(reviews)

        if results:

            summary = analyzer.summarize_sentiment(results)

            col1, col2, col3 = st.columns(3)

            col1.metric("😊 Positive", summary["Positive"])
            col2.metric("😞 Negative", summary["Negative"])
            col3.metric("😐 Neutral", summary["Neutral"])

            for item in results:

                st.markdown(
                    f"**{item['sentiment']}** — {item['review']}"
                )

                st.caption(item["reason"])

        else:
            st.warning("Could not analyze the reviews. Please try again.")

    else:
        st.warning("Please enter at least one customer review.")
        
# PRODUCT REVIEW ANALYSIS
if "review_analysis" in st.session_state:

    st.subheader("⭐ Product Rating Analysis")

    results = st.session_state["review_analysis"]

    if results:

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Products Analyzed", len(results))

        with col2:
            average_rating = sum(
                item["rating"] for item in results
            ) / len(results)

            st.metric("Average Rating", f"{average_rating:.2f}/5")

        st.divider()

        for item in results:

            with st.container(border=True):

                st.markdown(f"### {item['name']}")

                st.write(f"⭐ Rating: {item['rating']}/5")

                st.write(f"📝 Reviews: {item['review_count']}")

                st.write(f"📊 Rating Status: {item['rating_status']}")

                st.write(f"🔥 Popularity: {item['popularity']}")

    else:
        st.info("No products available for analysis.")
# --------------------------------------------------
# WELCOME MESSAGE
# --------------------------------------------------

if not st.session_state.messages:

    st.markdown(
        '<p class="section-title">What are you shopping for today?</p>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("💻 **Laptops**\n\nFind laptops for coding, gaming and work.")

    with col2:
        st.info("📱 **Smartphones**\n\nExplore smartphones across budgets.")

    with col3:
        st.info("🎧 **Headphones**\n\nDiscover headphones and earbuds.")


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            for product in message.get("products", []):

                with st.container(border=True):

                    st.markdown(f"### {product['name']}")

                    st.markdown(
                        f"**₹{product['price']:,.0f}**"
                    )

                    st.write(
                        f"⭐ {product['rating']}/5 "
                        f"({product['rating_count']} reviews)"
                    )

                    st.caption(
                        f"Brand: {product['brand']} | "
                        f"Stock: {product['stock']}"
                    )

                    st.caption(
                        f"Specifications: {product['specifications']}"
                    )


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

user_input = st.chat_input(
    "Ask ShopMind to find your perfect product..."
)

if st.session_state.pending_prompt:

    user_input = st.session_state.pending_prompt
    st.session_state.pending_prompt = None


# --------------------------------------------------
# PROCESS CUSTOMER REQUEST
# --------------------------------------------------

if user_input:

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
                        {"Laptop": "Laptops", "Smartphone": "Smartphones",
                         "Smartwatch": "Smartwatches"}.get(category, category)
                        if category != "All Categories" else None
                    ),
                    budget_override=(
                        budget if budget < 150000 else None
                    )
                )

                response = result["response"]

                products = result.get("products", [])
                record_search(
                    query=user_input,
                    category=category if category != "All Categories" else None,
                    budget=budget if budget < 150000 else None,
                    products=products
                )

                # The comparison agent can return structured data.
                if isinstance(response, dict):
                    comparison = response
                    response = (
                        f"Comparing {len(products)} products. "
                        f"Lowest price: ₹{comparison['cheapest']['price']:,.0f}. "
                        f"Highest rated: {comparison['highest_rated']['name']}."
                    ) if comparison and products else "Not enough products to compare."

                st.markdown(response)

                # Display product cards.
                if products:

                    st.markdown("### 🛍️ Recommended Products")

                    columns = st.columns(2)

                    for index, product in enumerate(products):

                        with columns[index % 2]:

                            with st.container(border=True):

                                st.markdown(
                                    f"#### {product['name']}"
                                )

                                st.markdown(
                                    f"<div class='product-price'>"
                                    f"₹{product['price']:,.0f}"
                                    f"</div>",
                                    unsafe_allow_html=True
                                )

                                st.write(
                                    f"⭐ {product['rating']}/5"
                                )

                                st.caption(
                                    f"{product['rating_count']} reviews"
                                )

                                st.write(
                                    f"**Brand:** {product['brand']}"
                                )

                                st.write(
                                    f"**Stock:** {product['stock']}"
                                )

                                st.caption(
                                    product["specifications"]
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