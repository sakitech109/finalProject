import pyttsx3
import pywhatkit
import wikipedia
import webbrowser
import time
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def searchGoogle(query):
    if "google" in query:
        query = query.replace("jarvis", "").replace("google search", "").replace("google", "")
        speak("Searching on Google...")
        
        try:
            pywhatkit.search(query)
            speak("Here are the results.")
        except:
            speak("I couldn't search Google at the moment.")
        return

def searchYoutube(query):
    if "youtube" in query:
        speak("Searching on YouTube...")
        query = query.replace("youtube search", "").replace("youtube", "").replace("jarvis", "")
        web = f"https://www.youtube.com/results?search_query={query}"
        
        try:
            webbrowser.open(web)
            time.sleep(2)  # Delay to ensure page loads before playing
            pywhatkit.playonyt(query)
            speak("Playing on YouTube.")
        except:
            speak("I couldn't search YouTube at the moment.")
        return

def searchWikipedia(query):
    if "wikipedia" in query:
        speak("Searching on Wikipedia...")
        query = query.replace("wikipedia", "").replace("search wikipedia", "").replace("jarvis", "")

        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia...")
            print(results)
            speak(results)
        except:
            speak("I couldn't find anything on Wikipedia.")
        return
