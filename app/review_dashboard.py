import streamlit as st

from reviews.review_analyzer import ReviewAnalyzer
from reviews.review_sentiment import ReviewSentimentAnalyzer


def render_review_dashboard():

    st.subheader("⭐ Product Review Analysis")

    # PRODUCT RATING ANALYSIS
    if st.button("Analyze Product Ratings"):

        analyzer = ReviewAnalyzer()

        st.session_state["review_analysis"] = (
            analyzer.analyze_all_products()
        )

    results = st.session_state.get("review_analysis")

    if results is not None:

        if results:

            col1, col2 = st.columns(2)

            col1.metric(
                "Products Analyzed",
                len(results)
            )

            average_rating = sum(
                item["rating"] for item in results
            ) / len(results)

            col2.metric(
                "Average Rating",
                f"{average_rating:.2f}/5"
            )

            for item in results:

                with st.container(border=True):

                    st.markdown(f"### {item['name']}")

                    st.write(f"⭐ Rating: {item['rating']}/5")

                    st.write(
                        f"📝 Reviews: {item['review_count']}"
                    )

                    st.write(
                        f"📊 Status: {item['rating_status']}"
                    )

                    st.write(
                        f"🔥 Popularity: {item['popularity']}"
                    )

        else:
            st.info("No products available for analysis.")

    # CUSTOMER SENTIMENT ANALYSIS
    st.divider()

    st.subheader("💬 Customer Review Sentiment Analysis")

    review_text = st.text_area(
        "Enter customer reviews (one review per line)",
        placeholder=(
            "Battery life is excellent!\n"
            "The product is too expensive.\n"
            "Good performance for the price."
        )
    )

    if st.button("Analyze Customer Sentiment"):

        reviews = [
            review.strip()
            for review in review_text.splitlines()
            if review.strip()
        ]

        if not reviews:

            st.warning("Please enter at least one review.")

        else:

            analyzer = ReviewSentimentAnalyzer()

            with st.spinner("Gemini is analyzing reviews..."):

                results = analyzer.analyze_reviews(reviews)

            if results:

                summary = analyzer.summarize_sentiment(results)

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "😊 Positive",
                    summary["Positive"]
                )

                col2.metric(
                    "😞 Negative",
                    summary["Negative"]
                )

                col3.metric(
                    "😐 Neutral",
                    summary["Neutral"]
                )

                st.divider()

                for item in results:

                    st.markdown(
                        f"**{item['sentiment']}** — "
                        f"{item['review']}"
                    )

                    st.caption(item["reason"])

            else:

                st.warning(
                    "Could not analyze reviews. Please try again."
                )