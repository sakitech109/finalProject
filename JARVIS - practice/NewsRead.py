# import requests
# import pyttsx3
# import speech_recognition as sr
#
# # Initialize text-to-speech engine
# engine = pyttsx3.init("sapi5")
# voices = engine.getProperty("voices")
# engine.setProperty("voice", voices[0].id)
# engine.setProperty("rate", 170)
#
# def speak(audio):
#     """Convert text to speech"""
#     engine.say(audio)
#     engine.runAndWait()
#
# def takeCommand():
#     """Recognize voice command"""
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening for news category...")
#         speak("Which category of news do you want? Business, Health, Technology, Sports, Entertainment, or Science?")
#         r.pause_threshold = 1
#         r.energy_threshold = 1000
#         try:
#             audio = r.listen(source, timeout=8, phrase_time_limit=5)
#             category = r.recognize_google(audio, language='en-in')
#             print(f"Recognized Category: {category}")
#             return category.lower().strip()
#         except sr.UnknownValueError:
#             speak("I didn't catch that. Can you repeat the category?")
#             return "none"
#         except sr.RequestError:
#             speak("There was an issue connecting to the recognition service.")
#             return "none"
#
# def latestnews():
#     """Fetch and read detailed news explanations"""
#     api_key = "pub_73493e5325ab33ff8e7caaf0ad04f7e4c5821"  # Your API Key
#
#     api_dict = {
#         "business": f"https://newsdata.io/api/1/news?apikey={api_key}&q=business",
#         "entertainment": f"https://newsdata.io/api/1/news?apikey={api_key}&q=entertainment",
#         "health": f"https://newsdata.io/api/1/news?apikey={api_key}&q=health",
#         "science": f"https://newsdata.io/api/1/news?apikey={api_key}&q=science",
#         "sports": f"https://newsdata.io/api/1/news?apikey={api_key}&q=sports",
#         "technology": f"https://newsdata.io/api/1/news?apikey={api_key}&q=technology"
#     }
#
#     category = takeCommand()
#
#     if category == "none":
#         return  # Exit if recognition fails
#
#     url = api_dict.get(category)
#
#     if not url:
#         speak("Sorry, I couldn't find news for that category. Please try again.")
#         return
#
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Check for request errors
#         news_data = response.json()
#
#         # Extract news articles
#         articles = news_data.get("results", [])  # 'results' instead of 'articles'
#
#         if not articles:
#             speak("Sorry, no news articles are available at the moment.")
#             return
#
#         speak(f"Here are the top {min(5, len(articles))} news stories in {category}.")
#
#         for i, article in enumerate(articles[:5]):  # Limit to 5 articles
#             title = article.get("title", "No title available")
#             description = article.get("description", "No details available")
#             news_url = article.get("link", "")
#
#             print(f"\nNews {i+1}: {title}\n")
#             print(f"Details: {description}\n")
#             if news_url:
#                 print(f"Read more: {news_url}\n")
#
#             speak(f"News {i+1}: {title}. {description}")
#
#             if i < len(articles) - 1:
#                 speak("Do you want to hear more? Say yes or no.")
#                 choice = takeCommand()
#                 if "no" in choice:
#                     break
#
#         speak("That's all for now.")
#     except requests.exceptions.RequestException as e:
#         speak("Sorry, I couldn't fetch the news at the moment.")
#         print(f"Error fetching news: {e}")
#
# # Call latestnews() to test
# if __name__ == "__main__":
#     latestnews()
import requests
import pyttsx3
import speech_recognition as sr

# Initialize text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)

def speak(audio):
    """Convert text to speech"""
    engine.say(audio)
    engine.runAndWait()

def askNewsCategory():
    """Ask for a news category"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for news category...")
        speak("Which category of news do you want? Business, Health, Technology, Sports, Entertainment, or Science?")
        r.pause_threshold = 1
        r.energy_threshold = 1000
        try:
            audio = r.listen(source, timeout=8, phrase_time_limit=5)
            category = r.recognize_google(audio, language='en-in')
            print(f"Recognized Category: {category}")
            return category.lower().strip()
        except sr.UnknownValueError:
            speak("I didn't catch that. Can you repeat the category?")
            return "none"
        except sr.RequestError:
            speak("There was an issue connecting to the recognition service.")
            return "none"

def takeSimpleCommand():
    """Recognize simple voice commands like 'yes' or 'no' without prompting for category"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 1000
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=3)
            query = r.recognize_google(audio, language='en-in')
            print(f"Recognized: {query}")
            return query.lower().strip()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return "none"
        except sr.RequestError:
            speak("There was a problem connecting to the service.")
            return "none"

def latestnews():
    """Fetch and read detailed news explanations"""
    api_key = "pub_73493e5325ab33ff8e7caaf0ad04f7e4c5821"  # Your API Key

    api_dict = {
        "business": f"https://newsdata.io/api/1/news?apikey={api_key}&q=business",
        "entertainment": f"https://newsdata.io/api/1/news?apikey={api_key}&q=entertainment",
        "health": f"https://newsdata.io/api/1/news?apikey={api_key}&q=health",
        "science": f"https://newsdata.io/api/1/news?apikey={api_key}&q=science",
        "sports": f"https://newsdata.io/api/1/news?apikey={api_key}&q=sports",
        "technology": f"https://newsdata.io/api/1/news?apikey={api_key}&q=technology"
    }

    category = askNewsCategory()

    if category == "none":
        return

    url = api_dict.get(category)
    if not url:
        speak("Sorry, I couldn't find news for that category. Please try again.")
        return

    try:
        response = requests.get(url)
        response.raise_for_status()
        news_data = response.json()

        articles = news_data.get("results", [])

        if not articles:
            speak("Sorry, no news articles are available at the moment.")
            return

        speak(f"Here are the top {min(5, len(articles))} news stories in {category}.")

        for i, article in enumerate(articles[:5]):
            title = article.get("title", "No title available")
            description = article.get("description", "No details available")
            news_url = article.get("link", "")

            print(f"\nNews {i+1}: {title}\n")
            print(f"Details: {description}\n")
            if news_url:
                print(f"Read more: {news_url}\n")

            speak(f"News {i+1}: {title}. {description}")

            if i < len(articles) - 1:
                speak("Do you want to hear more? Say yes or no.")
                choice = takeSimpleCommand()
                if "no" in choice:
                    break
                elif "yes" not in choice:
                    speak("I'll take that as a no.")
                    break

        speak("That's all for now.")
    except requests.exceptions.RequestException as e:
        speak("Sorry, I couldn't fetch the news at the moment.")
        print(f"Error fetching news: {e}")

# Run the news fetcher
if __name__ == "__main__":
    latestnews()
