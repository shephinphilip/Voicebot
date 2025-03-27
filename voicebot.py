import chainlit as cl
import speech_recognition as sr
import pyttsx3
from openai import OpenAI
import asyncio
import os
import threading

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

speech_lock = threading.Lock()
client = None

def speak(text: str):
    with speech_lock:
        try:
            print(f"Speaking: {text}")
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Speech error: {e}")

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
            question = recognizer.recognize_google(audio)
            print(f"You said: {question}")
            return question.lower()
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            return "Sorry, there was an error with the speech service."
        except sr.WaitTimeoutError:
            return "I didn't hear anything. Please try again."

def get_gpt_response(question: str) -> str:
    if client is None:
        return "Please provide your OpenAI API key by typing 'key: sk-...' in the chat."
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
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
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

def handle_question(question: str) -> str:
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

welcome_sent = False  # Global flag

@cl.on_chat_start
async def start():
    global welcome_sent
    # Check if the welcome message was already sent.
    if welcome_sent:
        return
    welcome_sent = True

    welcome_msg = (
        "Hello! I'm voice bot, built by Shephin Philip. Speak to me, and I'll reply with "
        "voice and text—try asking about my life story or superpowers! If you haven't yet, "
        "please enter your OpenAI API key by typing 'key: sk-...' in the chat."
    )
    print("Sending welcome message")
    await cl.Message(content=welcome_msg).send()
    speak(welcome_msg)
    
    # Inform the user to provide an API key (if not using sidebar)
    await cl.Message(
        content="Please enter your OpenAI API key by typing 'key: sk-...' in the chat."
    ).send()
    
    print("Starting continuous listening task")
    asyncio.create_task(continuous_listening())


async def continuous_listening():
    print("Starting continuous listening")
    retry_count = 0
    error_messages = [
        "sorry, i didn't catch that.",
        "sorry, there was an error with the speech service.",
        "i didn't hear anything. please try again."
    ]
    while True:
        try:
            question = await asyncio.to_thread(listen)
            print(f"Processing question: {question}")
            if question in error_messages:
                retry_count += 1
                if retry_count >= 3:
                    response = "No input received for 3 attempts. Shutting down..."
                    await cl.Message(content=response).send()
                    speak(response)
                    import sys; sys.exit(0)
                else:
                    await cl.Message(content=question).send()
                    speak(question)
                    continue
            else:
                retry_count = 0

            if any(phrase in question for phrase in ["exit", "quit", "bye", "goodbye"]):
                response = "Goodbye for now! Catch you later!"
                await cl.Message(content=response).send()
                speak(response)
                import sys; sys.exit(0)

            await cl.Message(content=f"You said: {question}").send()
            response = handle_question(question)
            await cl.Message(content=response).send()
            speak(response)
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"Error in continuous listening: {e}")
            await cl.Message(content="Something went wrong—let's try that again!").send()
            await asyncio.sleep(1)

@cl.on_message
async def main(message: cl.Message):
    global client

    # Check if the user typed "key: " at the start of their message
    if message.content.lower().startswith("key:"):
        user_key = message.content.split("key:", 1)[1].strip()
        try:
            client = OpenAI(api_key=user_key)
            await cl.Message(content="API key updated! You can now chat.").send()
        except Exception as e:
            err_msg = f"Invalid API key: {e}"
            print(err_msg)
            await cl.Message(content=err_msg).send()
        return

    # Otherwise, treat it as a normal user message
    if message.content:
        response = handle_question(message.content.lower())
        await cl.Message(content=response).send()
        speak(response)

def check_ffmpeg():
    import subprocess
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except FileNotFoundError:
        print("FFmpeg not found. Please install FFmpeg using: winget install ffmpeg (on Windows)")
        return False
    return True

if __name__ == "__main__":
    if not check_ffmpeg():
        print("Please install FFmpeg and try again.")
        exit(1)
    cl.run()
