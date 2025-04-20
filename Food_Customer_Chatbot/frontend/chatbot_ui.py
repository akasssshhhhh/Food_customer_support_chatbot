import streamlit as st
import time
from datetime import datetime
from get_chatbot_response import get_chatbot_response

st.set_page_config(page_title="🍕 Food Chatbot", page_icon="🤖")
st.title("🍔 Welcome to Food Chatbot!")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Styling
st.markdown("""
    <style>
    /* Ensure shiny white background for the entire page */
    body, .main {
        background-color: #ffffff;  /* Shiny white background */
        color: #111111;
    }

    .chat-container {
        display: flex;
        flex-direction: column;
    }

    .chat-bubble {
        max-width: 80%;
        padding: 10px 15px;
        margin: 10px;
        border-radius: 20px;
        display: inline-block;
        font-size: 16px;
        line-height: 1.5;
        color: black;
        word-wrap: break-word;
    }

    .user-bubble {
        background-color: #DCF8C6;
        align-self: flex-end;
        text-align: right;
    }

    .bot-bubble {
        background-color: #F1F0F0;
        align-self: flex-start;
        text-align: left;
    }

    .avatar {
        font-size: 20px;
        margin-right: 5px;
        vertical-align: middle;
    }

    .timestamp {
        font-size: 12px;
        color: #888;
        margin-top: -5px;
        margin-bottom: 10px;
    }

    .typing {
        font-style: italic;
        color: gray;
        animation: blink 1s infinite;
    }

    @keyframes blink {
        0%   { opacity: 0.2; }
        50%  { opacity: 1; }
        100% { opacity: 0.2; }
    }

    /* Styling for input box with shiny white background */
    .stTextInput > div > div > input {
        background-color: #ffffff;  /* Shiny white background */
        padding: 10px;
        border-radius: 8px;
        color: #111111;
        border: 2px solid black;  /* Black border for the question box */
    }

    /* Add black border to the outer container of the input box */
    .stTextInput > div {
        border: 2px solid black;  /* Black border around the entire input box */
        border-radius: 8px;
    }

    /* Hide Streamlit's default submit button */
    div[data-testid="stFormSubmitButton"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Chat input inside form (only Enter to submit)
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here...", key="input", placeholder="E.g. What are your vegetarian options?")
    submitted = st.form_submit_button("")

if submitted and user_input.strip():
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.chat_history.append(("user", user_input, timestamp))

    # Typing animation
    placeholder = st.empty()
    with st.spinner("🤖 Bot is typing..."):
        for dots in [".", "..", "..."]:
            placeholder.markdown(f"<div class='typing'>🤖 Typing{dots}</div>", unsafe_allow_html=True)
            time.sleep(0.4)

    response = get_chatbot_response(user_input)
    bot_message = response.get("response", "Oops! Something went wrong.")
    timestamp = datetime.now().strftime("%H:%M")
    st.session_state.chat_history.append(("bot", bot_message, timestamp))

    placeholder.empty()

# Display chat history
for sender, msg, timestamp in st.session_state.chat_history:
    bubble_class = "user-bubble" if sender == "user" else "bot-bubble"
    avatar = "👤" if sender == "user" else "🤖"

    st.markdown(
        f"""
        <div class='chat-container'>
            <div class='chat-bubble {bubble_class}'>
                <span class='avatar'>{avatar}</span> {msg}
            </div>
            <div class='timestamp'>{timestamp}</div>
        </div>
        """, unsafe_allow_html=True
    )

# Auto-scroll to bottom
st.markdown("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)
