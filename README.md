# QWQ-32B AI Chatbot

A Streamlit-based chatbot that uses the QWQ-32B model from OpenRouter for intelligent conversations.

## Features

- Powered by QWQ-32B, a reasoning model from the Qwen series
- Excels at complex reasoning and problem-solving
- Clean, user-friendly interface
- No API key required for users - ready to use immediately
- Conversation history maintained during the session

## Deployment

This app is designed to be deployed on Streamlit Cloud with the owner's API key securely stored in Streamlit secrets.

### Setting up Streamlit Secrets

1. In Streamlit Cloud, go to your app settings
2. Navigate to the "Secrets" section
3. Add your OpenRouter API key in this format:
   ```
   OPENROUTER_API_KEY = "sk-or-v1-your-api-key-here"
   ```

## Local Development

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.streamlit/secrets.toml` file with your OpenRouter API key
4. Run the app: `streamlit run main.py`

## About QWQ-32B

QWQ-32B is a reasoning model from the Qwen series. Compared with conventional instruction-tuned models, QWQ is capable of thinking and reasoning, achieving significantly enhanced performance in downstream tasks, especially hard problems.

This model excels at:
- Complex reasoning
- Problem-solving
- Detailed explanations
- Nuanced understanding 