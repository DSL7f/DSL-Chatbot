import streamlit as st
import requests
import json
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

# Function to make API calls to OpenRouter
def call_openrouter_api(messages):
    try:
        # Get API key from Streamlit secrets
        api_key = st.secrets["OPENROUTER_API_KEY"]
        
        # Prepare the request
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://streamlit-app.com",
            "X-Title": "QWQ-32B AI Chatbot"
        }
        data = {
            "model": "qwen/qwq-32b",
            "route": "groq",  # Specify Groq as the provider for better throughput
            "messages": messages
        }
        
        # Make the API call
        response = requests.post(url, headers=headers, json=data)
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            error_text = response.text
            print(f"API Error: {response.status_code} - {error_text}")
            return f"Error: Unable to get a response (Status code: {response.status_code}). Details: {error_text}"
    
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Error details: {error_details}")
        return "I'm sorry, I encountered an error while processing your request. Please try again later."

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
    # Convert messages to the format expected by the API
    formatted_messages = [
        {"role": m["role"], "content": m["content"]} 
        for m in messages
    ]
    
    # Call the OpenRouter API
    return call_openrouter_api(formatted_messages)

# User input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_text = generate_response(st.session_state.messages)
            st.markdown(response_text)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text}) 