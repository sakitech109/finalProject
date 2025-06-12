import pywhatkit
import pyttsx3
import datetime
import speech_recognition as sr
from datetime import datetime
import difflib

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
if voices and isinstance(voices, (list, tuple)):
    engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 180)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speak("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 3000
        try:
            audio = r.listen(source, timeout=4, phrase_time_limit=10)

            query = r.recognize_google(audio, language='en-in')
            print(f"You Said: {query}")
            return query.lower().strip()
        except sr.UnknownValueError:
            speak("I didn't catch that. Please say it again.")
            return "none"
        except sr.RequestError:
            speak("There was an issue connecting to the recognition service.")
            return "none"

def sendMessage():
    contacts = {
        "ali": "+923203939567",
        "usama": "+923042422121"
    }

    speak("Who do you want to message?")
    print("Available contacts:", ", ".join(contacts.keys()))
    recipient_input = takeCommand()

    # Use fuzzy matching to find the closest contact name
    matched = difflib.get_close_matches(recipient_input, contacts.keys(), n=1, cutoff=0.5)

    if not matched:
        # Try partial match if no fuzzy match
        for name in contacts:
            if name in recipient_input:
                matched = [name]
                break

    if not matched:
        speak("I couldn't find that contact. Please try again.")
        return

    recipient = matched[0]

    speak("What is the message?")
    message = takeCommand()

    if message == "none":
        speak("Message was not recognized. Try again.")
        return

    now = datetime.now()
    send_hour = now.hour
    send_minute = now.minute + 2
    if send_minute >= 60:
        send_hour = (send_hour + 1) % 24
        send_minute %= 60

    speak(f"Sending message to {recipient}: {message}")
    try:
        pywhatkit.sendwhatmsg(contacts[recipient], message, send_hour, send_minute, wait_time=15)
        speak("Message sent successfully.")
    except Exception as e:
        speak("There was an error sending the message.")
        print(f"Error: {e}")

if __name__ == "__main__":
    sendMessage()

