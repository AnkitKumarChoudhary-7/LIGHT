# core.py
import os
import datetime
import logging
from dotenv import load_dotenv
import pyttsx3
import speech_recognition as sr
from openai import OpenAI
import screen_brightness_control as sbc
import subprocess
import webbrowser
import ctypes
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load API key
try:
    load_dotenv()
except FileNotFoundError:
    logger.error("Error: .env file not found. AI features will not work.")
    print("Error: .env file not found. AI features will not work.")
    API_KEY = None
    client = None
else:
    API_KEY = os.getenv("OPENAI_API_KEY")
    if not API_KEY:
        print("Warning: OPENAI_API_KEY not found in .env file. AI features will not work.")
        client = None
    else:
        client = OpenAI(api_key=API_KEY)

def say(text: str):
    """Speak the given text aloud."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Select a different voice if more than one is available
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)

    print(f"Light says: {text}")
    engine.say(text)
    engine.runAndWait()


# ---------- AI (very small wrapper) ----------
chat_history = [
    {
        "role": "system",
        "content": (
            "You are Light, a helpful, concise voice assistant running on Ankit's Windows PC. "
            "Keep answers short and clear, speak like a friendly AI companion."
        ),
    }
]

def ai(prompt: str) -> str:
    global chat_history
    if not client:
        return "Sorry sir, AI features are not available. Please check your OpenAI API key configuration."
    
    messages = chat_history + [{"role": "user", "content": prompt}]
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        answer = response.choices[0].message.content
        chat_history.append({"role": "user", "content": prompt})
        chat_history.append({"role": "assistant", "content": answer})
        # Keep history short
        if len(chat_history) > 20:
            chat_history = [chat_history[0]] + chat_history[-18:]
        return answer
    except Exception as e:
        print("AI error:", e)
        # Handle specific API errors
        if "insufficient_quota" in str(e):
            return "Sorry sir, I've reached my API limit. Please check your OpenAI account."
        elif "rate_limit" in str(e):
            return "Sorry sir, I'm getting too many requests. Please wait a moment."
        else:
            return "Sorry sir, I had trouble thinking just now."

# ---------- Speech recognition ----------
def takeCommand():
    """Listen and return recognized text (or None)."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return None
    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        print("Couldn't understand audio.")
        say("Sorry, I couldn't understand. Please say that again.")
        return None
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        say("There was a problem with the speech service, sir.")
        return None
    except Exception as e:
        print("Unexpected error in takeCommand:", e)
        return None

# ---------- Brightness helpers using screen_brightness_control ----------
def set_brightness(percent: int):
    try:
        # Input validation
        if not isinstance(percent, (int, float)):
            raise ValueError("Brightness must be a number")
        percent = max(0, min(100, int(percent)))  # Clamp between 0-100
        
        sbc.set_brightness(percent)
        say(f"Brightness set to {percent} percent, sir.")
    except Exception as e:
        print("set_brightness error:", e)
        say("I couldn't change brightness, sir.")

def get_brightness():
    try:
        return sbc.get_brightness()[0]
    except Exception as e:
        print("get_brightness error:", e)
        return None

def increase_brightness(step: int = 10):
    try:
        current = get_brightness() or 0
        new_level = min(100, current + step)
        sbc.set_brightness(new_level)
        say(f"Brightness increased to {new_level} percent, sir.")
    except Exception as e:
        print("increase_brightness error:", e)
        say("I couldn't increase brightness, sir.")

def decrease_brightness(step: int = 10):
    try:
        current = get_brightness() or 0
        new_level = max(0, current - step)
        sbc.set_brightness(new_level)
        say(f"Brightness decreased to {new_level} percent, sir.")
    except Exception as e:
        print("decrease_brightness error:", e)
        say("I couldn't decrease brightness, sir.")

# ---------- Volume Control (FINAL, SIMPLE, WORKING) ----------

def _get_volume():
    devices = AudioUtilities.GetSpeakers()
    return devices.EndpointVolume


def volume_up():
    try:
        volume = _get_volume()
        current = volume.GetMasterVolumeLevelScalar()
        new = min(current + 0.1, 1.0)
        volume.SetMasterVolumeLevelScalar(new, None)
        say(f"Volume increased to {int(new * 100)} percent, sir.")
    except Exception as e:
        print("volume_up error:", e)
        say("I couldn't increase volume, sir.")


def volume_down():
    try:
        volume = _get_volume()
        current = volume.GetMasterVolumeLevelScalar()
        new = max(current - 0.1, 0.0)
        volume.SetMasterVolumeLevelScalar(new, None)
        say(f"Volume decreased to {int(new * 100)} percent, sir.")
    except Exception as e:
        print("volume_down error:", e)
        say("I couldn't decrease volume, sir.")


def mute_volume():
    try:
        volume = _get_volume()
        volume.SetMute(1, None)
        say("Volume muted, sir.")
    except Exception as e:
        print("mute error:", e)
        say("I couldn't mute volume, sir.")


def unmute_volume():
    try:
        volume = _get_volume()
        volume.SetMute(0, None)
        say("Volume unmuted, sir.")
    except Exception as e:
        print("unmute error:", e)
        say("I couldn't unmute volume, sir.")

# ---------- System Commands ----------
def lock_pc():
    try:
        ctypes.windll.user32.LockWorkStation()
        say("PC locked, sir.")
    except Exception as e:
        print("lock_pc error:", e)
        say("I couldn't lock the PC, sir.")

def shutdown_system():
    try:
        subprocess.run(["shutdown", "/s", "/t", "0"], check=True)
    except Exception as e:
        print("shutdown_system error:", e)
        say("I couldn't shutdown the system, sir.")

def restart_system():
    try:
        subprocess.run(["shutdown", "/r", "/t", "0"], check=True)
    except Exception as e:
        print("restart_system error:", e)
        say("I couldn't restart the system, sir.")

def sleep_system():
    try:
        subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0", "1", "0"], check=True)
    except Exception as e:
        print("sleep_system error:", e)
        say("I couldn't put the system to sleep, sir.")

def sign_out():
    try:
        subprocess.run(["shutdown", "/l"], check=True)
    except Exception as e:
        print("sign_out error:", e)
        say("I couldn't sign out, sir.")

# ---------- Media Commands ----------
def play_youtube_song():
    try:
        webbrowser.open("https://www.youtube.com")
        say("Opening YouTube, sir.")
    except Exception as e:
        print("play_youtube_song error:", e)
        say("I couldn't open YouTube, sir.")

def playMusic():
    try:
        webbrowser.open("https://open.spotify.com")
        say("Opening Spotify, sir.")
    except Exception as e:
        print("playMusic error:", e)
        say("I couldn't open music player, sir.")