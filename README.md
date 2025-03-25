# Voicebot

## Summary

Voicebot is an interactive AI voice assistant built using Chainlit. It converts spoken input into text, processes queries with OpenAI's GPT model, and responds with both text and speech. Throughout the development process, we integrated asynchronous event handling, speech recognition, text-to-speech synthesis, and robust error handling to deliver a seamless, conversational user experience.

## Architecture

Voicebot leverages several key components:

- **Chainlit:** A framework for building interactive chat applications. It manages the frontend interface and asynchronous event handling.
- **Speech Recognition:** Utilizes the `SpeechRecognition` package and the Google Web Speech API to capture and convert audio input into text.
- **Text-to-Speech:** Uses `pyttsx3` to convert text responses into spoken audio, with threading locks to ensure non-overlapping speech output.
- **OpenAI GPT API:** Processes user queries by generating dynamic responses using a predefined personality, enhancing the conversational tone.
- **Async & Threading:** `asyncio` handles non-blocking operations (continuous listening) while `threading` prevents concurrent speech synthesis.
- **FFmpeg:** Ensures compatibility with various audio formats required for processing audio inputs.

### Architecture Diagram

```
         ┌─────────────────┐
         │   User Speech   │
         └─────────────────┘
                   │
                   ▼
       ┌──────────────────────┐
       │  Speech Recognition  │
       └──────────────────────┘
                   │
                   ▼
       ┌──────────────────────┐        ┌─────────────────────┐
       │ Chainlit Interface   │◄──────►│  Text-to-Speech     │
       └──────────────────────┘        └─────────────────────┘
                   │
                   ▼
       ┌──────────────────────┐
       │  Handle Question     │◄─────────────┐
       └──────────────────────┘              │
                   │                         │
                   ▼                         │
       ┌──────────────────────┐             │
       │  OpenAI GPT API      │             │
       └──────────────────────┘             │
                   │                         │
                   ▼                         │
       ┌──────────────────────┐             │
       │  Generate Response   │─────────────┘
       └──────────────────────┘
```

## Design Decisions & Approach

- **Modular Structure:** Functions like `speak`, `listen`, and `handle_question` isolate core functionalities, making the code easy to understand, test, and extend.
- **Robust Error Handling:** The code includes retries for speech recognition errors (up to 3 attempts) and a graceful shutdown approach, assuring a reliable user experience even when facing input issues.
- **Asynchronous Processing:** Leveraging `asyncio` and Chainlit's event-driven architecture allows continuous listening without blocking the application.
- **Concurrency Management:** Thread locks ensure that text-to-speech operations do not overlap, preserving clear and coherent audio output.
- **User-Controlled Exit:** The design monitors voice commands like "exit", "quit", "bye", or "goodbye" to terminate the session immediately, ensuring user control.
- **Environment and Dependency Management:** A `.env` file is used for managing sensitive keys, while dependencies like FFmpeg guarantee smooth audio processing.

## Installation

### Prerequisites
- **Python 3.8+**
- **FFmpeg:** Ensure FFmpeg is installed and available in your system's PATH.
  - **Windows:**
    ```bash
    winget install ffmpeg
    ```
  - **Other OS:** Refer to [FFmpeg documentation](https://ffmpeg.org/download.html).

### Setup Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/Voicebot.git
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

3. **Install Dependencies:**
   ```bash
   pip install chainlit SpeechRecognition pyttsx3 openai python-dotenv
   pip install PyAudio
   ```
   *Note: If PyAudio installation fails on Windows, download the appropriate wheel from [this site](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) and install it using pip.*

4. **Configure Environment Variables:**
   Create a `.env` file in the project root with the following content:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Running Voicebot

Start the Voicebot using Chainlit with the following command:

```bash
chainlit run voicebot.py
```

This command launches the Chainlit server, loads the voice bot interface, and begins continuous voice input processing. The bot responds both via text and spoken output.

## Additional Information

- **Error Handling:** If no valid input is received for 3 consecutive attempts, Voicebot shuts down automatically.
- **Exit Functionality:** Commands like "exit", "quit", "bye", or "goodbye" immediately terminate the session.
- **Continuous Listening:** The application uses asynchronous processing to listen for input continuously while ensuring clear, non-overlapping speech output.

## Acknowledgements

- **Chainlit:** For the robust interactive chat framework.
- **SpeechRecognition & PyAudio:** For enabling seamless voice input.
- **pyttsx3:** For efficient text-to-speech conversion.
- **OpenAI GPT:** For powering dynamic, engaging conversational responses.
- Special thanks to Shephin Philip for the vision behind this project.
