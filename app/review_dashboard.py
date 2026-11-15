import streamlit as st

from reviews.review_analyzer import ReviewAnalyzer
from reviews.review_sentiment import ReviewSentimentAnalyzer


def render_review_dashboard():

    st.markdown("# ⭐ Review Intelligence")

    st.caption(
        "Understand product ratings, popularity, "
        "and customer sentiment with AI."
    )

    # -----------------------------------------
    # PRODUCT RATING ANALYSIS
    # -----------------------------------------

    st.markdown("## 📊 Product Rating Analytics")

    if st.button(
        "✨ Analyze Product Ratings",
        use_container_width=True,
    ):

        analyzer = ReviewAnalyzer()

        st.session_state["review_analysis"] = (
            analyzer.analyze_all_products()
        )

    results = st.session_state.get("review_analysis")

    if results is not None:

        if results:

            average_rating = sum(
                item["rating"] for item in results
            ) / len(results)

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Products Analyzed",
                    len(results),
                )

            with col2:
                st.metric(
                    "Average Product Rating",
                    f"⭐ {average_rating:.2f}/5",
                )

            st.divider()

            st.markdown("### 🏆 Product Performance")

            for item in results:

                with st.container(border=True):

                    st.markdown(f"### {item['name']}")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(
                            "Rating",
                            f"⭐ {item['rating']}/5",
                        )

                    with col2:
                        st.metric(
                            "Reviews",
                            item["review_count"],
                        )

                    with col3:
                        st.metric(
                            "Popularity",
                            item["popularity"],
                        )

                    st.caption("Rating Status")

                    st.info(item["rating_status"])

        else:

            st.info("No products available for analysis.")

    # -----------------------------------------
    # CUSTOMER SENTIMENT ANALYSIS
    # -----------------------------------------

    st.divider()

    st.markdown("## 💬 Customer Sentiment Intelligence")

    st.write(
        "Enter customer reviews below. ShopMind will use "
        "Gemini to classify their sentiment."
    )

    review_text = st.text_area(
        "Customer Reviews",
        placeholder=(
            "Battery life is excellent!\n"
            "The product is too expensive.\n"
            "Good performance for the price."
        ),
        height=150,
    )

    if st.button(
        "🤖 Analyze Customer Sentiment",
        use_container_width=True,
    ):

        reviews = [
            review.strip()
            for review in review_text.splitlines()
            if review.strip()
        ]

        if not reviews:

            st.warning("Please enter at least one review.")

        else:

            analyzer = ReviewSentimentAnalyzer()

            with st.spinner(
                "ShopMind AI is analyzing customer reviews..."
            ):

                try:

                    sentiment_results = analyzer.analyze_reviews(
                        reviews
                    )

                    if sentiment_results:

                        summary = analyzer.summarize_sentiment(
                            sentiment_results
                        )

                        st.session_state["sentiment_results"] = (
                            sentiment_results
                        )

                        st.session_state["sentiment_summary"] = summary

                    else:

                        st.warning(
                            "Could not analyze reviews. Please try again."
                        )

                except Exception as error:

                    print("Sentiment Analysis Error:", error)

                    st.error(
                        "Unable to analyze reviews. Please try again."
                    )

    # -----------------------------------------
    # SENTIMENT RESULTS
    # -----------------------------------------

    summary = st.session_state.get("sentiment_summary")
    sentiment_results = st.session_state.get("sentiment_results")

    if summary and sentiment_results:

        st.divider()

        st.markdown("### 📈 Sentiment Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "😊 Positive",
                summary["Positive"],
            )

        with col2:
            st.metric(
                "😞 Negative",
                summary["Negative"],
            )

        with col3:
            st.metric(
                "😐 Neutral",
                summary["Neutral"],
            )

        st.divider()

        st.markdown("### 📝 Individual Review Analysis")

        for item in sentiment_results:

            with st.container(border=True):

                st.markdown(
                    f"**{item['sentiment']}**"
                )

                st.write(item["review"])

                st.caption(item["reason"])