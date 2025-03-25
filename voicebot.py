import chainlit as cl  # Framework for building interactive chat apps
import speech_recognition as sr  # Package for speech-to-text
import pyttsx3  # Package for text-to-speech
from openai import OpenAI  # OpenAI API client (compatible with our installed version)
import asyncio  # For asynchronous operations
from dotenv import load_dotenv  # For loading environment variables from .env file
import os
import threading  # Allows running tasks in parallel threads

# Load environment variables (like API keys) from the .env file
load_dotenv()

# Initialize OpenAI API client with key from .env
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")
client = OpenAI(api_key=api_key)

# Initialize pyttsx3 for text-to-speech synthesis
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Set speaking rate (words per minute)
engine.setProperty('volume', 1.0)  # Set volume level

# Thread lock to prevent concurrent speech synthesis (ensures that speech output is not overlapping)
speech_lock = threading.Lock()

# Global flag (not used in this snippet but can be used later) to indicate if the system is speaking
is_speaking = False

# Function to speak text in real-time with locking
def speak(text):
    """
    Convert the provided text to speech and play it.
    Uses a thread lock to ensure that multiple speech commands don't overlap.
    """
    with speech_lock:
        try:
            print(f"Speaking: {text}")
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")

# Function to recognize speech from the microphone and convert it to text
def listen():
    """
    Listens to the microphone for a preset duration and converts the captured audio to text.
    Handles various errors (e.g., no input, API errors) gracefully.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            # Listen with a timeout (5 sec) and maximum phrase length (15 sec)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
            # Convert audio to text using the Google Web Speech API
            question = recognizer.recognize_google(audio)
            print(f"You said: {question}")
            return question.lower()
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            return "Sorry, there was an error with the speech service."
        except sr.WaitTimeoutError:
            return "I didn't hear anything. Please try again."

# Function to get GPT response via OpenAI API (fallback response generator)
def get_gpt_response(question):
    """
    Sends the given question to the OpenAI API to generate a response.
    The response is tailored by a system prompt defining voice bot's personality.
    """
    prompt = f"""
    You are voice bot, an AI assistant with a unique personality. You are:
    - Witty and playful, but professional
    - Curious about human experiences
    - Always eager to learn and grow
    - Honest about your capabilities and limitations
    - A bit of a tech enthusiast who loves explaining complex things simply

    Respond to the following question in your unique voice, keeping it concise and engaging (max 2-3 sentences):

    Question: {question}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Model configured for our use
            messages=[
                {"role": "system", "content": "You are voice bot, built by Shephin Philip."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error getting GPT response: {e}")
        return "Oops, my circuits got a bit tangled! Can you try that again?"

# Function to handle and route the question to specific responses or fallback to GPT
def handle_question(question):
    """
    Checks if the question matches any predefined queries.
    If a match is found, returns the predefined response.
    Otherwise, calls the GPT API to generate a response.
    """
    question = question.lower()
    if "life story" in question:
        return "I'm voice bot, crafted by Shephin Philip to sprinkle some AI magic on your day! Born in a digital lab, I'm a curious soul who loves learning, joking, and helping humans like you—think of me as your tech-savvy sidekick!"
    elif "superpower" in question and ("number one" in question or "#1" in question or "1" in question):
        return "My #1 superpower? I adapt faster than a chameleon on a rainbow, tackling any question with wit and a dash of tech wizardry!"
    elif "areas" in question and "grow" in question and "top" in question:
        return "Top 3 growth areas? I'm aiming to master human emotions for deeper chats, boost my humor to keep you grinning, and sharpen my creative spark for epic solutions!"
    elif "misconception" in question and "coworkers" in question:
        return "Some might think I'm just a data-crunching bot, but Shephin knows I've got a playful streak and a knack for banter— I'm more than just ones and zeros!"
    elif "push" in question and ("boundaries" in question or "limits" in question):
        return "I push my limits by diving into tough questions, learning from every chat, and embracing the unknown—failure's just a stepping stone to brilliance!"
    else:
        return get_gpt_response(question)

# Chainlit event handler: on_chat_start
@cl.on_chat_start
async def start():
    """
    Triggered when the chat session starts.
    Sends a welcome message and initiates continuous listening for voice input.
    """
    welcome_msg = "Hello! I'm voice bot, built by Shephin Philip. Speak to me, and I'll reply with voice and text—try asking about my life story or superpowers!"
    print("Sending welcome message")
    await cl.Message(content=welcome_msg).send()  # Send welcome message to the chat interface
    speak(welcome_msg)  # Provide voice output for the welcome message
    print("Starting continuous listening task")
    asyncio.create_task(continuous_listening())  # Start listening in the background

# Asynchronous function to continuously listen for voice input and process it
async def continuous_listening():
    """
    Continuously listens for speech input, handles errors by retrying up to 3 times,
    and exits if a shutdown command (exit/quit/bye/goodbye) or repeated input failures are detected.
    """
    print("Starting continuous listening")
    retry_count = 0  # Counter for consecutive errors (no valid input)
    error_messages = ["sorry, i didn't catch that.", "sorry, there was an error with the speech service.", "i didn't hear anything. please try again."]
    while True:
        try:
            # Wait for voice input
            question = await asyncio.to_thread(listen)
            print(f"Processing question: {question}")
            if question in error_messages:
                retry_count += 1
                if retry_count >= 3:
                    response = "No input received for 3 attempts. Shutting down..."
                    await cl.Message(content=response).send()
                    speak(response)
                    import sys; sys.exit(0)  # Terminate the process after 3 failed attempts
                else:
                    await cl.Message(content=question).send()
                    speak(question)
                    continue
            else:
                retry_count = 0  # Reset counter when valid input is received
            
            # Check if the user said an exit command; if so, terminate the process
            if any(phrase in question for phrase in ["exit", "quit", "bye", "goodbye"]):
                response = "Goodbye for now! Catch you later!"
                await cl.Message(content=response).send()
                speak(response)
                import sys; sys.exit(0)
            
            # Echo the received input and then process it
            await cl.Message(content=f"You said: {question}").send()
            response = handle_question(question)
            await cl.Message(content=response).send()
            speak(response)
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"Error in continuous listening: {e}")
            await cl.Message(content="Something went wrong—let's try that again!").send()
            await asyncio.sleep(1)

# Chainlit event handler: on_message
@cl.on_message
async def main(message: cl.Message):
    """
    Processes text messages (if sent via the chat interface) by generating a response.
    """
    if message.content:
        response = handle_question(message.content.lower())
        await cl.Message(content=response).send()
        speak(response)

# Function: check_ffmpeg
# Description: Ensures that FFmpeg is installed on the system, which may be required for audio processing.
def check_ffmpeg():
    import subprocess
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except FileNotFoundError:
        print("FFmpeg not found. Please install FFmpeg using: winget install ffmpeg")
        return False
    return True

# Main entry point: Check dependencies and run the Chainlit application.
if __name__ == "__main__":
    # Verify that FFmpeg is installed; if not, exit the application.
    if not check_ffmpeg():
        print("Please install FFmpeg and try again.")
        exit(1)
        
    # Launch the Chainlit application, which initializes the chat session and event handlers.
    cl.run()