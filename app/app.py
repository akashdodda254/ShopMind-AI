import streamlit as st

from agents.orchestrator import ShopMindOrchestrator


# Page configuration
st.set_page_config(
    page_title="ShopMind AI",
    page_icon="🛍️",
    layout="wide"
)


# Initialize ShopMind only once.
@st.cache_resource
def initialize_shopmind():
    return ShopMindOrchestrator()


shopmind = initialize_shopmind()


# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []


# Header
st.title("🛍️ ShopMind AI")
st.subheader("Your Intelligent Shopping Assistant")

st.write(
    "Discover products, explore recommendations "
    "and find the right products for your budget."
)

st.divider()


# Sidebar
with st.sidebar:

    st.title("ShopMind")

    st.write("Your personal AI shopping assistant.")

    st.divider()

    st.subheader("What can I help you find?")

    suggestions = [
        "Find gaming laptops under 75000",
        "Recommend smartphones",
        "Find headphones",
        "Compare laptops under 80000"
    ]

    for suggestion in suggestions:

        if st.button(suggestion, use_container_width=True):
            st.session_state.pending_prompt = suggestion

    st.divider()

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pop("pending_prompt", None)
        st.rerun()


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
user_input = st.chat_input(
    "What are you looking for today?"
)

# Handle sidebar suggestions.
if "pending_prompt" in st.session_state:
    user_input = st.session_state.pop("pending_prompt")


# Process user request
if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner("ShopMind is thinking..."):

            try:
                response = shopmind.process_request(user_input)

            except Exception as error:
                print("ShopMind Error:", error)

                response = (
                    "Sorry, something went wrong. "
                    "Please try again."
                )

            st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })