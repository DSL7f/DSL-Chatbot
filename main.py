import streamlit as st
from openai import OpenAI

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

# Try to get API key from Streamlit secrets
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
    # Initialize OpenAI client with OpenRouter base URL
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    api_key_status = "API key loaded from secrets ✅"
except Exception as e:
    client = None
    api_key_status = f"Error loading API key: {str(e)}"

# Add a sidebar with information and settings
with st.sidebar:
    st.title("OpenRouter AI Chatbot")
    st.markdown("""
    This chatbot uses OpenRouter to access various AI models.
    
    OpenRouter provides access to models like QWQ-32B, GPT-4o, Claude, and more through a unified API.
    
    The chat history is maintained during your session.
    """)
    
    # Display API key status
    st.subheader("API Key Status")
    st.info(api_key_status)
    
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
    
    # Test connection button
    if st.button("Test OpenRouter Connection"):
        if client:
            try:
                # Simple test request
                response = client.chat.completions.create(
                    model="openai/gpt-3.5-turbo",
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=5
                )
                st.success("OpenRouter connection successful! ✅")
            except Exception as e:
                st.error(f"OpenRouter connection failed: {str(e)}")
        else:
            st.error("Client not initialized. Check API key.")

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
            completion = client.chat.completions.create(
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
            response = client.images.generate(
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
    if not client:
        return "Error: OpenRouter client is not initialized. Please check your API key in Streamlit secrets.", None
    
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