# Voicebot

## Summary

Voicebot is an interactive AI chatbot built using Chainlit. It provides a simple web interface where users can chat with an AI assistant powered by OpenAI's GPT model. The bot features a witty and engaging personality, making conversations both informative and entertaining.

## Features

- **Web-Based Interface:** Easy-to-use chat interface accessible through any web browser
- **Simple Setup:** No complex installations or coding knowledge required
- **API Key Management:** Secure input of OpenAI API key through the web interface
- **Engaging Personality:** Witty and professional responses with a tech-savvy touch
- **Error Handling:** Robust error management for API issues and invalid inputs

## Quick Start

1. **Visit the Web App:**
   - Open your web browser and navigate to the Voicebot web application
   - No installation required!

2. **Enter Your API Key:**
   - When you first open the app, you'll be prompted to enter your OpenAI API key
   - Your API key is only used for the current session and is not stored
   - Get your API key from [OpenAI's website](https://platform.openai.com/api-keys)

3. **Start Chatting:**
   - Once your API key is validated, you can start chatting with Voicebot
   - Type your messages in the chat interface
   - Voicebot will respond with engaging, context-aware answers

## Deployment

### Option 1: Deploy on Chainlit Cloud (Recommended)

1. **Create a Chainlit Account:**
   - Visit [Chainlit Cloud](https://cloud.chainlit.io)
   - Sign up for a free account

2. **Install Chainlit CLI:**
   ```bash
   pip install chainlit
   ```

3. **Login to Chainlit:**
   ```bash
   chainlit login
   ```

4. **Deploy Your App:**
   ```bash
   chainlit deploy
   ```
   - Follow the prompts to configure your deployment
   - Your app will be available at `https://your-app-name.chainlit.app`

### Option 2: Deploy on Your Own Server

1. **Prepare Your Server:**
   - Ensure Python 3.8+ is installed
   - Set up a virtual environment
   - Install dependencies:
     ```bash
     pip install chainlit openai python-dotenv
     ```

2. **Configure Environment Variables:**
   Create a `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   CHAINLIT_AUTH_ENABLED=false  # Disable authentication for public access
   ```

3. **Run the Server:**
   ```bash
   chainlit run voicebot.py -w
   ```
   - The `-w` flag enables web access
   - Your app will be available at `http://your-server-ip:8000`

4. **Set Up a Reverse Proxy (Optional):**
   - Use Nginx or Apache to serve the app with SSL
   - Configure your domain name

### Option 3: Deploy on Railway.app

1. **Create a Railway Account:**
   - Visit [Railway.app](https://railway.app)
   - Sign up and create a new project

2. **Connect Your Repository:**
   - Link your GitHub repository
   - Railway will automatically detect the Python project

3. **Configure Environment Variables:**
   - Add your OpenAI API key in Railway's dashboard
   - Set `CHAINLIT_AUTH_ENABLED=false` for public access

4. **Deploy:**
   - Railway will automatically build and deploy your app
   - Your app will be available at `https://your-app-name.railway.app`

## Technical Details

### Architecture

Voicebot uses a simple but effective architecture:

- **Frontend:** Chainlit provides a modern, responsive web interface
- **Backend:** Python-based server handling message processing
- **AI Processing:** OpenAI's GPT-3.5 Turbo model for generating responses
- **Security:** API keys are handled securely and not stored

### Design Decisions

- **Web-First Approach:** Chose web interface over voice for maximum accessibility
- **Simple Authentication:** API key input through web interface for easy setup
- **Error Prevention:** Built-in validation and error handling for API key and responses
- **User Experience:** Clean, intuitive interface with immediate feedback

## Development Setup (Optional)

If you want to run Voicebot locally:

1. **Install Python 3.8+**

2. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/Voicebot.git
   cd Voicebot
   ```

3. **Create and Activate Virtual Environment:**
   ```bash
   python -m venv venv
   ```
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies:**
   ```bash
   pip install chainlit openai python-dotenv
   ```

5. **Run the Application:**
   ```bash
   chainlit run voicebot.py
   ```

## Security Notes

- API keys are only used for the current session and are not stored
- All communication is handled securely
- No personal data is collected or stored

## Troubleshooting

- **API Key Issues:** Make sure your API key is valid and has sufficient credits
- **Connection Problems:** Check your internet connection
- **Browser Issues:** Try refreshing the page or using a different browser
- **Deployment Issues:** Check the Chainlit logs for detailed error messages

## Acknowledgements

- **Chainlit:** For the robust web interface framework
- **OpenAI:** For providing the powerful GPT model
- Special thanks to Shephin Philip for the vision behind this project
