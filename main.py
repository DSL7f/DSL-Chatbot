import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Get the API key from environment variable with fallback to None
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Set page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    .stChatMessage {
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key" not in st.session_state:
    st.session_state.api_key = OPENROUTER_API_KEY

if "client" not in st.session_state:
    # Will be initialized later when we have the API key
    st.session_state.client = None

if "rerun_requested" not in st.session_state:
    st.session_state.rerun_requested = False

if "model_type" not in st.session_state:
    st.session_state.model_type = "Text"

# Add a sidebar with information and settings
with st.sidebar:
    st.title("AI Chatbot")
    st.markdown("""
    This chatbot uses OpenRouter to access various AI models.
    
    You can have a conversation with the AI and ask it various questions.
    
    The chat history is maintained during your session.
    """)
    
    # API Key input if not set in environment
    if not st.session_state.api_key:
        st.warning("No API key found in environment variables.")
        api_key = st.text_input(
            "Enter your OpenRouter API key:",
            type="password",
            help="Get an API key from https://openrouter.ai/keys"
        )
        
        if api_key:
            st.session_state.api_key = api_key
            st.success("API key set successfully!")
            st.session_state.rerun_requested = True
    else:
        st.success("API key is configured ✅")
    
    # Model selection
    st.subheader("Model Selection")
    model_type = st.radio(
        "Choose model type:",
        ["Text", "Image Generation"]
    )
    st.session_state.model_type = model_type
    
    if model_type == "Text":
        selected_model = st.selectbox(
            "Select text model:",
            ["qwen/qwq-32b", "openai/gpt-4o", "anthropic/claude-3-opus", "mistralai/mistral-medium"]
        )
    else:
        selected_model = st.selectbox(
            "Select image model:",
            ["stability/sdxl", "openai/dall-e-3"]
        )
    
    st.session_state.selected_model = selected_model
    
    # Add a clear button to reset the conversation
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.rerun_requested = True

# Initialize the client if we have an API key but no client
if st.session_state.api_key and not st.session_state.client:
    try:
        st.session_state.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=st.session_state.api_key,
        )
    except Exception as e:
        st.error(f"Error initializing client: {str(e)}")
        st.session_state.client = None

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and message.get("image_url"):
            st.image(message["image_url"])
        else:
            st.markdown(message["content"])

# Function to generate text response
def generate_text_response(messages):
    try:
        with st.spinner("Thinking..."):
            completion = st.session_state.client.chat.completions.create(
                model=st.session_state.selected_model,
                messages=[
                    {"role": m["role"], "content": m["content"]} 
                    for m in messages
                ]
            )
            return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return "Sorry, I encountered an error while processing your request. Please try again later."

# Function to generate image
def generate_image(prompt):
    try:
        with st.spinner("Generating image..."):
            response = st.session_state.client.images.generate(
                model=st.session_state.selected_model,
                prompt=prompt,
                size="1024x1024",
                n=1
            )
            # Return the image URL
            return response.data[0].url
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Main response generation function
def generate_response(prompt):
    if not st.session_state.client:
        return "Please provide an OpenRouter API key to continue.", None
    
    if st.session_state.model_type == "Text":
        return generate_text_response(st.session_state.messages), None
    else:
        image_url = generate_image(prompt)
        if image_url:
            return f"I've generated an image based on your prompt: '{prompt}'", image_url
        else:
            return "Failed to generate an image. Please try again or use a different prompt.", None

# User input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        response_text, image_url = generate_response(prompt)
        st.markdown(response_text)
        if image_url:
            st.image(image_url)
    
    # Add assistant response to chat history
    assistant_message = {"role": "assistant", "content": response_text}
    if image_url:
        assistant_message["image_url"] = image_url
    st.session_state.messages.append(assistant_message)

# Handle rerun requests at the end of the script
if st.session_state.rerun_requested:
    st.session_state.rerun_requested = False
    st.rerun() 