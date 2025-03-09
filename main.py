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
def call_openrouter_api(messages, stream=False, use_groq=True):
    try:
        # Get API key from Streamlit secrets
        api_key = st.secrets["OPENROUTER_API_KEY"]
        
        # Prepare the request
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://your-app-domain.com",  # Required by OpenRouter
            "X-Title": "QWQ-32B AI Chatbot"  # Helps with OpenRouter analytics
        }
        
        # Don't add Accept header for streaming as it can cause issues
        if stream:
            headers["Accept"] = "text/event-stream"
            
        data = {
            "model": "qwen/qwq-32b",
            "messages": messages
        }
        
        # Add Groq routing if specified
        if use_groq:
            data["route"] = "groq"  # Use Groq provider for better throughput
            
        # Add streaming parameter if needed
        if stream:
            data["stream"] = True
        
        # Print request data for debugging
        print(f"Request URL: {url}")
        print(f"Request Headers: {headers}")
        print(f"Request Data: {json.dumps(data, indent=2)}")
        
        # Make the API call
        response = requests.post(url, headers=headers, json=data, stream=stream)
        
        # Check if the request was successful
        if response.status_code == 200:
            if stream:
                return response  # Return the response object for streaming
            else:
                return response.json()["choices"][0]["message"]["content"]
        else:
            error_message = f"API Error: {response.status_code} - {response.text}"
            print(error_message)
            # Try to parse the error response for more details
            try:
                error_json = response.json()
                print(f"Error details: {json.dumps(error_json, indent=2)}")
            except:
                pass
            return f"Error: Unable to get a response (Status code: {response.status_code}). Please check the logs for details."
    
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

# Function to process streaming response
def process_streaming_response(response):
    full_response = ""
    response_placeholder = st.empty()
    
    try:
        for line in response.iter_lines():
            if not line:
                continue
                
            line_text = line.decode('utf-8')
            # Print raw line for debugging
            print(f"Raw streaming line: {line_text}")
            
            # Handle SSE format
            if line_text.startswith('data: '):
                line_data = line_text[6:]  # Remove 'data: ' prefix
                
                # Check for stream end
                if line_data == "[DONE]":
                    break
                
                try:
                    chunk = json.loads(line_data)
                    # Print chunk for debugging
                    print(f"Parsed chunk: {json.dumps(chunk, indent=2)}")
                    
                    if 'choices' in chunk and len(chunk['choices']) > 0:
                        choice = chunk['choices'][0]
                        
                        # Handle different response formats
                        if 'delta' in choice:
                            delta = choice['delta']
                            if 'content' in delta and delta['content'] is not None:
                                content = delta['content']
                                full_response += content
                                response_placeholder.markdown(full_response)
                        elif 'message' in choice:
                            message = choice['message']
                            if 'content' in message and message['content'] is not None:
                                content = message['content']
                                full_response += content
                                response_placeholder.markdown(full_response)
                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {str(e)} for line: {line_data}")
                    continue
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Streaming error: {str(e)}\n{error_details}")
        if not full_response:
            full_response = "Error processing streaming response. Please try again."
            response_placeholder.markdown(full_response)
    
    return full_response

# Function to generate text response
def generate_response(messages):
    # Convert messages to the format expected by the API
    formatted_messages = [
        {"role": m["role"], "content": m["content"]} 
        for m in messages
    ]
    
    try:
        # First try with streaming enabled and Groq provider
        response = call_openrouter_api(formatted_messages, stream=True, use_groq=True)
        
        # Process the streaming response
        if isinstance(response, requests.Response):
            return process_streaming_response(response)
        else:
            # If we got a string response, it's likely an error message
            print(f"Streaming with Groq failed, response: {response}")
            
            # If streaming failed with a 400 error, try without streaming
            if "Error: Unable to get a response (Status code: 400)" in response:
                print("Trying without streaming but still using Groq")
                non_streaming_response = call_openrouter_api(formatted_messages, stream=False, use_groq=True)
                
                # If that still fails, try without Groq
                if "Error: Unable to get a response" in non_streaming_response:
                    print("Trying without Groq provider")
                    return call_openrouter_api(formatted_messages, stream=False, use_groq=False)
                return non_streaming_response
            return response
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"Error in generate_response: {str(e)}\n{error_details}")
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
        # No need to display the response here as it's already displayed in the streaming function
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text}) 