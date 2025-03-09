import streamlit as st
from openai import OpenAI
import traceback

# Set page configuration
st.set_page_config(
    page_title="QWQ-32B AI Chatbot",
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
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session states if they don't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

if "client" not in st.session_state:
    # Try to initialize the client with the API key from Streamlit secrets
    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]
        # Simple client initialization without extra parameters
        st.session_state.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        # Test the client with a simple request
        test_response = st.session_state.client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Hello"}],
            max_tokens=5
        )
    except Exception as e:
        st.session_state.client = None
        st.error("Error initializing the chatbot. Please contact the administrator.")
        print(f"Error details: {traceback.format_exc()}")
        st.stop()

# Main app title and description
st.title("QWQ-32B AI Chatbot")
st.markdown("""
This chatbot uses the QWQ-32B model from OpenRouter, which excels at reasoning and complex problem-solving.
Ask any question and get a thoughtful response!
""")

# Sidebar with information
with st.sidebar:
    st.header("About QWQ-32B")
    st.markdown("""
    **QWQ-32B** is a reasoning model from the Qwen series. Compared with conventional instruction-tuned models, 
    QWQ is capable of thinking and reasoning, achieving significantly enhanced performance in downstream tasks, 
    especially hard problems.
    
    This model excels at:
    - Complex reasoning
    - Problem-solving
    - Detailed explanations
    - Nuanced understanding
    """)
    
    # Add a clear button to reset the conversation
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to generate text response
def generate_response(messages):
    try:
        with st.spinner("Thinking..."):
            completion = st.session_state.client.chat.completions.create(
                model="qwen/qwq-32b",
                messages=[
                    {"role": m["role"], "content": m["content"]} 
                    for m in messages
                ]
            )
            return completion.choices[0].message.content
    except Exception as e:
        error_details = traceback.format_exc()
        st.error("An error occurred while generating a response. Please try again later.")
        print(f"Error details: {error_details}")
        return "I'm sorry, I encountered an error while processing your request. Please try again later."

# User input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        response_text = generate_response(st.session_state.messages)
        st.markdown(response_text)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text}) 