import streamlit as st
from openai import OpenAI
import traceback

# Set page configuration
st.set_page_config(
    page_title="OpenRouter AI Chatbot",
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

# Initialize session states if they don't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

if "model_type" not in st.session_state:
    st.session_state.model_type = "Text"

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "qwen/qwq-32b"

if "manual_api_key" not in st.session_state:
    st.session_state.manual_api_key = ""

if "client" not in st.session_state:
    st.session_state.client = None

# Function to initialize the OpenRouter client
def initialize_client(api_key):
    try:
        # Clean the API key (remove any whitespace or quotes)
        api_key = api_key.strip().strip('"\'')
        
        # Initialize the client
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        
        # Test the client with a simple request
        test_response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Hello"}],
            max_tokens=5
        )
        
        return client, True, "API key verified and connection successful ✅"
    except Exception as e:
        error_details = traceback.format_exc()
        return None, False, f"Error initializing client: {str(e)}\n\nDetails: {error_details}"

# Main app title
st.title("OpenRouter AI Chatbot")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    
    # API Key Management
    st.subheader("API Key")
    
    # Try to get API key from Streamlit secrets
    secrets_key_status = ""
    client_initialized = False
    
    try:
        if "OPENROUTER_API_KEY" in st.secrets:
            api_key = st.secrets["OPENROUTER_API_KEY"]
            st.success("API key found in Streamlit secrets")
            
            # Initialize client with the secret key
            client, success, message = initialize_client(api_key)
            if success:
                st.session_state.client = client
                client_initialized = True
                st.success(message)
            else:
                st.error(f"Secret API key error: {message}")
                secrets_key_status = "invalid"
        else:
            st.warning("No API key found in Streamlit secrets")
            secrets_key_status = "missing"
    except Exception as e:
        st.error(f"Error accessing secrets: {str(e)}")
        secrets_key_status = "error"
    
    # If secrets didn't work, show manual input
    if not client_initialized:
        st.write("Enter your OpenRouter API key manually:")
        manual_key = st.text_input(
            "API Key",
            type="password",
            value=st.session_state.manual_api_key,
            help="Get an API key from https://openrouter.ai/keys"
        )
        
        if manual_key:
            st.session_state.manual_api_key = manual_key
            
            # Initialize client with the manual key
            client, success, message = initialize_client(manual_key)
            if success:
                st.session_state.client = client
                client_initialized = True
                st.success(message)
            else:
                st.error(f"Manual API key error: {message}")
    
    # Debug information
    st.subheader("Debug Information")
    st.write(f"Secrets Status: {secrets_key_status}")
    st.write(f"Client Initialized: {client_initialized}")
    
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
        st.rerun()

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
                extra_headers={
                    "HTTP-Referer": "https://streamlit-app.com",  # optional
                    "X-Title": "OpenRouter AI Chatbot",           # optional
                },
                messages=[
                    {"role": m["role"], "content": m["content"]} 
                    for m in messages
                ]
            )
            return completion.choices[0].message.content
    except Exception as e:
        st.error(f"OpenRouter API Error: {str(e)}")
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
        st.error(f"OpenRouter API Error: {str(e)}")
        return None

# Main response generation function
def generate_response(prompt):
    if not st.session_state.client:
        return "Error: OpenRouter client is not initialized. Please check your API key in the sidebar.", None
    
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