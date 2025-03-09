# OpenRouter AI Chatbot

This is a Streamlit-based chatbot that uses OpenRouter to access various AI models, including QWQ-32B for text generation and image generation models like SDXL.

## About OpenRouter

OpenRouter is a unified API that gives you access to hundreds of AI models through a single endpoint. It provides access to models from various providers including OpenAI, Anthropic, Google, and many open-source models.

**Important Note**: OpenRouter uses the OpenAI API format, which is why we use the OpenAI Python library to connect to it. This doesn't mean we're using OpenAI directly - we're using OpenRouter's service which provides access to many different models.

## Features

- Text generation with multiple model options (QWQ-32B, GPT-4o, Claude-3-Opus, etc.)
- Image generation capabilities
- Secure API key management using Streamlit secrets
- Fallback to manual API key input if secrets aren't configured
- Detailed error reporting and debugging information
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

3. Set up your OpenRouter API key using Streamlit secrets:
   - Create a `.streamlit` directory in your project root if it doesn't exist
   - Create a `secrets.toml` file inside the `.streamlit` directory
   - Add your OpenRouter API key to the file:
     ```toml
     OPENROUTER_API_KEY = "sk-or-v1-your-api-key-here"
     ```
   - Make sure to include the quotes around your API key
   - **IMPORTANT**: Add `.streamlit/secrets.toml` to your `.gitignore` file to prevent committing your API key

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
   - Add your API key in the following format (exactly as shown):
     ```toml
     OPENROUTER_API_KEY = "sk-or-v1-your-api-key-here"
     ```
   - Make sure to:
     - Include the quotes around your API key
     - Use the exact variable name `OPENROUTER_API_KEY`
     - Include spaces around the equals sign
   - Click "Save" to store your secret

5. Deploy the app by clicking "Deploy!"

## API Key Options

The application provides two ways to use your OpenRouter API key:

1. **Streamlit Secrets (Recommended)**: Configure your API key in Streamlit Cloud secrets or in a local `.streamlit/secrets.toml` file.

2. **Manual Input**: If the secrets method fails or isn't configured, you can enter your API key directly in the sidebar. This is useful for testing or if you're having issues with the secrets configuration.

## Troubleshooting

If you're experiencing issues with the API key:

1. **Check the Debug Information** in the sidebar, which shows:
   - Secrets Status: Whether the API key was found in secrets
   - Client Initialized: Whether the OpenRouter client was successfully initialized

2. **Check the Secret Format**:
   - The secret must be in this exact format:
     ```toml
     OPENROUTER_API_KEY = "sk-or-v1-your-api-key-here"
     ```
   - Common mistakes to avoid:
     - Missing quotes around the API key
     - Typos in the variable name (must be exactly `OPENROUTER_API_KEY`)
     - Extra spaces or characters in the API key
     - Comments or other text in the secrets section

3. **Try Manual Input**:
   - If the secrets method isn't working, enter your API key manually in the sidebar
   - The app will test the key immediately and show if it's valid

4. **Restart the App**:
   - After setting or updating secrets, restart your Streamlit app
   - In the Streamlit Cloud dashboard, click on the three dots next to your app and select "Reboot app"

## How It Works

The application connects to OpenRouter's API using the OpenAI Python library because OpenRouter uses the OpenAI API format. This allows us to access a wide range of models through a single, consistent interface.

The application tries to load your API key from Streamlit's secrets management system first. If that fails, it provides a fallback option to enter your API key manually in the sidebar.

## Usage

1. Ensure your API key is configured (either via secrets or manual input)
2. Select the model type (Text or Image Generation) from the sidebar
3. Choose a specific model from the dropdown menu
4. Type your message in the chat input box and press Enter
5. View the AI's response in the chat
6. Use the "Clear Conversation" button in the sidebar to start a new conversation

## Important Notes

- All usage will be billed to the OpenRouter account associated with the API key
- Consider implementing usage limits or monitoring to prevent unexpected costs
- Keep your API key secure and never commit it to version control

## License

[MIT License](LICENSE)