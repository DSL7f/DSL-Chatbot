import streamlit as st
from openai import OpenAI
import time

# Set page configuration
st.set_page_config(
    page_title="QWQ-32B Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 1.5rem; 
        border-radius: 0.5rem; 
        margin-bottom: 1rem; 
        display: flex;
        flex-direction: row;
        align-items: flex-start;
    }
    .chat-message.user {
        background-color: #2b313e;
    }
    .chat-message.assistant {
        background-color: #475063;
    }
    .chat-message .avatar {
        width: 20%;
        padding-right: 1rem;
    }
    .chat-message .avatar img {
        max-width: 78px;
        max-height: 78px;
        border-radius: 50%;
        object-fit: cover;
    }
    .chat-message .message {
        width: 80%;
        padding: 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )

client = get_openai_client()

# App title
st.title("🤖 QWQ-32B Chatbot")
st.subheader("Chat with Qwen's QWQ-32B model via OpenRouter")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to generate response
def generate_response(prompt):
    try:
        with st.spinner("Thinking..."):
            completion = client.chat.completions.create(
                model="qwen/qwq-32b",
                messages=[
                    {"role": m["role"], "content": m["content"]} 
                    for m in st.session_state.messages
                ]
            )
            return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return "Sorry, I encountered an error while processing your request."

# User input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        response = generate_response(prompt)
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Add a sidebar with information
with st.sidebar:
    st.title("About")
    st.markdown("""
    This chatbot uses Qwen's QWQ-32B model via OpenRouter.
    
    You can have a conversation with the AI and ask it various questions.
    
    The chat history is maintained during your session.
    """)
    
    # Add a clear button to reset the conversation
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.experimental_rerun() 