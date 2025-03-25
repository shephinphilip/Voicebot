# Voicebot

Voicebot is an interactive AI voice assistant built using Chainlit. It converts your spoken input into text, processes your queries using OpenAI's GPT model, and responds with both text and speech. Voicebot is designed with a playful, engaging personality and is ideal for demonstrating voice-enabled AI interactions.

## Architecture

Voicebot leverages several key components:
- **Chainlit:** A framework for building interactive chat applications. It provides the frontend interface and manages asynchronous events.
- **Speech Recognition:** Utilizes the `SpeechRecognition` package to capture audio from your microphone and convert it to text using the Google Web Speech API.
- **Text-to-Speech:** Uses `pyttsx3` to convert text responses into spoken audio output.
- **OpenAI GPT API:** Processes user queries by generating dynamic responses based on a predefined personality. The response is then relayed as text and converted to speech.
- **Async and Threading:** Uses `asyncio` for non-blocking operations (continuous listening, processing) and `threading` to prevent overlapping speech synthesis.
- **Environment Configuration:** Sensitive data, such as the OpenAI API key, is managed using a `.env` file.
- **FFmpeg Dependency:** Required for audio processing; ensures compatibility with various audio formats.


## Installation

### Prerequisites
- **Python 3.8+**
- **FFmpeg:** Make sure FFmpeg is installed and available in your system’s PATH.  
  - **Windows:** You can use:  
    ```bash
    winget install ffmpeg
    ```
  - **Other OS:** Refer to [FFmpeg documentation](https://ffmpeg.org/download.html).

### Steps
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/shephinphilip/Voicebot.git
   cd Voicebot
   ```

2. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv venv
   ```
   - **On Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **On macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

3. **Install the Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *If you encounter issues with PyAudio on Windows, download the appropriate wheel from [this site](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and install it using pip.*

4. **Configure Environment Variables:**
   - In `.env` file in the project root with the following content:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

## Running Voicebot

Launch Voicebot using Chainlit:
```bash
chainlit run voicebot.py
```
This command starts the Chainlit server, opens the frontend interface, and begins continuous voice input processing. Once the welcome message is displayed, speak into your microphone. Voicebot will demonstrate both speech-to-text conversion and text-to-speech response functionality.

## Usage

- **Voice Input:** Voicebot continuously listens for your spoken queries. 
- **Text Output:** Your query and the bot's response are shown in the chat interface.
- **Speech Output:** Responses are also spoken aloud.
- **Shutdown Behavior:**
  - If no valid input is detected for 3 consecutive attempts, Voicebot will shut down automatically.
  - You can also say "exit", "quit", "bye", or "goodbye" to terminate the conversation.

## Troubleshooting

- **No Audio Input/Output:** Make sure your microphone is working and not being used by another application.
- **FFmpeg Issues:** Ensure FFmpeg is correctly installed and in your PATH.
- **PyAudio Installation:** If installation fails on Windows, download a precompiled wheel from the website mentioned above.



## Acknowledgements

- **Chainlit:** For providing a robust framework for interactive chat applications.
- **SpeechRecognition & PyAudio:** For enabling voice input.
- **pyttsx3:** For text-to-speech functionality.
- **OpenAI:** For powering the GPT-based conversational responses.
