import streamlit as st
from openai import OpenAI
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

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

# Initialize session states
if "api_key" not in st.session_state:
    # Try to get API key from environment variable
    default_api_key = os.getenv("OPENROUTER_API_KEY", "")
    st.session_state.api_key = default_api_key

if "client" not in st.session_state:
    st.session_state.client = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "rerun_requested" not in st.session_state:
    st.session_state.rerun_requested = False

# Initialize OpenAI client
def get_openai_client(api_key):
    if not api_key:
        return None
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

# Add a sidebar with information and settings
with st.sidebar:
    st.title("Settings")
    
    # API Key input with a form
    with st.form("api_key_form"):
        api_key = st.text_input(
            "OpenRouter API Key",
            type="password",
            help="Enter your OpenRouter API key. Get one at https://openrouter.ai/keys"
        )
        submit_button = st.form_submit_button("Submit API Key")
        
        if submit_button:
            if api_key:
                st.session_state.api_key = api_key
                st.session_state.client = get_openai_client(api_key)
                st.success("API key updated successfully!")
                st.session_state.rerun_requested = True
            else:
                st.error("Please enter an API key")
    
    # Display current API key status
    if st.session_state.api_key:
        st.success("API key is set ✅")
    else:
        st.warning("Please enter your OpenRouter API key to continue")
    
    # Add a clear button to reset the conversation
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.rerun_requested = True
    
    st.title("About")
    st.markdown("""
    This chatbot uses Qwen's QWQ-32B model via OpenRouter.
    
    You can have a conversation with the AI and ask it various questions.
    
    The chat history is maintained during your session.
    
    To use this chatbot, you need an OpenRouter API key.
    Sign up at [OpenRouter](https://openrouter.ai/) to get one.
    """)

# App title
st.title("🤖 QWQ-32B Chatbot")
st.subheader("Chat with Qwen's QWQ-32B model via OpenRouter")

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to generate response
def generate_response(prompt):
    if not st.session_state.client:
        return "Please enter your OpenRouter API key in the sidebar to continue."
    
    try:
        with st.spinner("Thinking..."):
            completion = st.session_state.client.chat.completions.create(
                model="qwen/qwq-32b",
                messages=[
                    {"role": m["role"], "content": m["content"]} 
                    for m in st.session_state.messages
                ]
            )
            return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return "Sorry, I encountered an error while processing your request. Please check your API key and try again."

# User input
if prompt := st.chat_input("What would you like to ask?"):
    # Check if API key is provided
    if not st.session_state.api_key:
        st.error("Please enter your OpenRouter API key in the sidebar to continue.")
    else:
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

# Initialize client if we have an API key but no client
if st.session_state.api_key and not st.session_state.client:
    st.session_state.client = get_openai_client(st.session_state.api_key)

# Handle rerun requests at the end of the script
if st.session_state.rerun_requested:
    st.session_state.rerun_requested = False
    st.rerun() 