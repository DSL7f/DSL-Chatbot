# AI Chatbot with OpenRouter

This is a Streamlit-based chatbot that uses OpenRouter to access various AI models, including QWQ-32B for text generation and image generation models like SDXL.

## Features

- Text generation with multiple model options (QWQ-32B, GPT-4o, Claude-3-Opus, etc.)
- Image generation capabilities
- No need for users to input their own API keys
- Clean, user-friendly interface
- Conversation history maintained during the session

## Setup

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
   - Replace the placeholder in the `.env` file with your actual API key:
     ```
     OPENROUTER_API_KEY=your_actual_api_key_here
     ```

4. Run the application:
   ```
   streamlit run main.py
   ```

5. Open your browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

## Deployment

For production deployment, make sure to set the `OPENROUTER_API_KEY` environment variable in your hosting platform:

- **Streamlit Cloud**: Add the secret in the app settings
- **Heroku**: Use config vars
- **AWS**: Use environment variables or AWS Secrets Manager

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