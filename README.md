# QWQ-32B Streamlit Chatbot

A modern, interactive chatbot built with Streamlit that uses Qwen's QWQ-32B model via OpenRouter API.

![Chatbot Screenshot](https://i.imgur.com/placeholder.png)

## Features

- 🤖 Interactive chat interface with Qwen's QWQ-32B model
- 💬 Persistent conversation history during your session
- 🎨 Clean, modern UI with custom styling
- 🔄 Conversation reset functionality
- ⚡ Optimized API calls with caching

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/qwq-chatbot.git
   cd qwq-chatbot
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenRouter API key (choose one method):
   
   **Option 1: Environment file**
   - Copy the example environment file: `cp .env.example .env`
   - Edit the `.env` file and add your OpenRouter API key
   
   **Option 2: Environment variable**
   - Set the environment variable directly:
     - Windows: `set OPENROUTER_API_KEY=your_api_key_here`
     - Linux/Mac: `export OPENROUTER_API_KEY=your_api_key_here`
   
   **Option 3: Input in the app**
   - Enter your API key directly in the app's sidebar when prompted

   > 📝 Note: You'll need to sign up at [OpenRouter](https://openrouter.ai/) to get an API key.

## Usage

Run the Streamlit app:
```
streamlit run main.py
```

This will launch a web interface (typically at http://localhost:8501) where you can interact with the chatbot.

## How It Works

The application uses:
- **Streamlit** for the web interface
- **OpenAI Python SDK** to connect to OpenRouter's API
- **Qwen's QWQ-32B model** for generating responses

The chat history is maintained during your session, allowing for contextual conversations.

## Customization

You can customize the chatbot by:
- Changing the model in `main.py` (replace `"qwen/qwq-32b"` with another model available on OpenRouter)
- Modifying the UI styling in the CSS section
- Adding additional features to the sidebar

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web app framework
- [OpenRouter](https://openrouter.ai/) for providing access to various AI models
- [Qwen](https://qwenlm.github.io/) for their QWQ-32B model