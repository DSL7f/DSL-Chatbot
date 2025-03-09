# AI Chatbot with OpenRouter

This is a Streamlit-based chatbot that uses OpenRouter to access various AI models, including QWQ-32B for text generation and image generation models like SDXL.

## Features

- Text generation with multiple model options (QWQ-32B, GPT-4o, Claude-3-Opus, etc.)
- Image generation capabilities
- Flexible API key configuration (environment variable or user input)
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
   - Replace the placeholder in the `.env` file with your actual API key:
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
   - Add a new secret with the key `OPENROUTER_API_KEY` and your API key as the value:
     ```
     OPENROUTER_API_KEY = "sk-or-v1-your-api-key-here"
     ```
   - Save the secret

5. Deploy the app.

If you don't set the API key as a secret, the app will still work, but users will need to input their own OpenRouter API key.

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

## Troubleshooting

- **API Key Error**: If you see an error about the API key not being set, make sure you've added it as a secret in Streamlit Cloud or entered it in the sidebar input field.
- **Model Not Found**: Ensure you're using a valid model ID from OpenRouter's available models.
- **Rate Limiting**: If you encounter rate limiting errors, you may need to upgrade your OpenRouter plan or implement rate limiting in your application.

## License

[MIT License](LICENSE)