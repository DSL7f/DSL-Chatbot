# OpenRouter AI Chatbot

This is a Streamlit-based chatbot that uses OpenRouter to access various AI models, including QWQ-32B for text generation and image generation models like SDXL.

## About OpenRouter

OpenRouter is a unified API that gives you access to hundreds of AI models through a single endpoint. It provides access to models from various providers including OpenAI, Anthropic, Google, and many open-source models.

**Important Note**: OpenRouter uses the OpenAI API format, which is why we use the OpenAI Python library to connect to it. This doesn't mean we're using OpenAI directly - we're using OpenRouter's service which provides access to many different models.

## Features

- Text generation with multiple model options (QWQ-32B, GPT-4o, Claude-3-Opus, etc.)
- Image generation capabilities
- Flexible API key configuration (Streamlit secrets, environment variables, or user input)
- Clean, user-friendly interface
- Conversation history maintained during the session

## Local Setup

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenRouter API key:
   - Get an API key from [OpenRouter](https://openrouter.ai/keys)
   - Create a `.env` file in the project root and add your API key:
     ```
     OPENROUTER_API_KEY=your_actual_api_key_here
     ```

4. Run the application:
   ```
   streamlit run main.py
   ```

5. Open your browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

## Deployment to Streamlit Cloud

1. Fork or push this repository to your GitHub account.

2. Log in to [Streamlit Cloud](https://streamlit.io/cloud).

3. Click "New app" and select your repository, branch, and main file path (`main.py`).

4. **IMPORTANT**: Set the OpenRouter API key as a secret:
   - In the app settings, go to the "Secrets" section
   - Add your API key in the following format:
     ```toml
     OPENROUTER_API_KEY = "sk-or-v1-your-api-key-here"
     ```
   - Make sure to include the quotes around your API key
   - The format must be exactly as shown above (with spaces around the equals sign)
   - Click "Save" to store your secret

5. Deploy the app by clicking "Deploy!"

## Troubleshooting Streamlit Cloud Deployment

If you're experiencing issues with the API key not being recognized in Streamlit Cloud:

1. **Check the secret format**:
   - The secret must be in this exact format:
     ```toml
     OPENROUTER_API_KEY = "sk-or-v1-your-api-key-here"
     ```
   - Include the quotes around the API key
   - Include spaces around the equals sign
   - Do not add any comments or extra characters

2. **Verify the API key**:
   - Make sure your OpenRouter API key is valid and active
   - Test it with the "Test OpenRouter Connection" button in the sidebar

3. **Restart the app**:
   - After setting or updating secrets, restart your Streamlit app
   - In the Streamlit Cloud dashboard, click on the three dots next to your app and select "Reboot app"

4. **Check the debug information**:
   - The app includes debug information in the sidebar
   - Look for success or error messages related to secrets and client initialization

## How It Works

The application connects to OpenRouter's API using the OpenAI Python library because OpenRouter uses the OpenAI API format. This allows us to access a wide range of models through a single, consistent interface.

The application is designed to check for the API key in the following order:
1. Streamlit secrets (for cloud deployment)
2. Environment variables (for local development)
3. User input (as a fallback)

This ensures that your app will work seamlessly in both local and cloud environments.

## Usage

1. Select the model type (Text or Image Generation) from the sidebar
2. Choose a specific model from the dropdown menu
3. Type your message in the chat input box and press Enter
4. View the AI's response in the chat
5. Use the "Clear Conversation" button in the sidebar to start a new conversation

## Important Notes

- All usage will be billed to the OpenRouter account associated with the API key
- Consider implementing usage limits or monitoring to prevent unexpected costs
- Keep your API key secure and never commit it to version control

## License

[MIT License](LICENSE)