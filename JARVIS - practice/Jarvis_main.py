import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QMovie, QPixmap, QFont
from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QPushButton
from PyQt5.QtCore import QThread, QByteArray
from PyQt5.uic import loadUiType
import pyttsx3
import speech_recognition as sr
from speech_recognition import Recognizer
r: Recognizer = sr.Recognizer()
import datetime
import os
import time
import webbrowser
import speedtest
import subprocess
import re
import pyautogui 
import random

# Initialize text-to-speech engine


engine = pyttsx3.init("sapi5")

# Get available voices
voices = engine.getProperty("voices")

# Check if any voices are available
if voices and isinstance(voices, (list, tuple)):
    engine.setProperty("voice", voices[0].id)
else:
    print("No voices available or returned object is not a list.")

engine.setProperty("rate", 180)


def speak(audio):
    print(f"Speaking: {audio}")
    QMetaObject.invokeMethod(main.text_log, "append", Qt.QueuedConnection, Q_ARG(str, f"<b>Jarvis:</b> {audio}"))
    engine.say(audio)
    engine.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good morning")
    elif hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good evening")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        QMetaObject.invokeMethod(main.text_log, "append", Qt.QueuedConnection, Q_ARG(str, "<b>Listening...</b>"))

        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=8, phrase_time_limit=5)
            print("Understanding...")
            query = r.recognize_google(audio, language='en-in')
            print(f"You Said: {query}\n")

            QMetaObject.invokeMethod(main.text_log, "append", Qt.QueuedConnection, Q_ARG(str, f"<b>You:</b> {query}"))
            return query.lower()
        except sr.UnknownValueError:
            QMetaObject.invokeMethod(main.text_log, "append", Qt.QueuedConnection, Q_ARG(str, "<b>Could not understand.</b>"))
            return "none"
        except sr.RequestError:
            speak("Could not request results, check your internet connection")
        except sr.WaitTimeoutError:
            speak("Listening timed out. Try speaking again.")
        return "none"



def latestnews():
    from NewsRead import latestnews
    latestnews()
    
def format_alarm_time(alarm_time):
    """ Normalize and validate alarm time """
    # Remove unnecessary spaces and convert to lowercase
    alarm_time = alarm_time.strip().lower()

    # Convert "a.m." and "p.m." to "AM" and "PM"
    alarm_time = alarm_time.replace("a.m.", "AM").replace("p.m.", "PM")
    
    # Convert to proper format if it's in "7:30 am" style
    match = re.match(r"(\d{1,2}):(\d{2})\s*(am|pm)?", alarm_time)
    if match:
        hours, minutes, period = match.groups()
        hours = int(hours)
        
        if period:
            period = period.upper()  # Ensure "AM/PM" is capitalized
            
            # Convert to 24-hour format if needed
            if period == "PM" and hours < 12:
                hours += 12
            elif period == "AM" and hours == 12:
                hours = 0
        
        return f"{hours:02}:{minutes}"  # Ensure format "HH:MM"
    
    return None  # Return None if invalid format

 



def set_alarm():
    """ Set alarm using only voice commands """
    speak("Set the alarm time. For example, say '7:30 AM' or '22:10'.")
    
    alarm_time = takeCommand()  # Listen for user input
    
    if alarm_time == "none":
        speak("I didn't hear the time. Please try again.")
        return

    # Format and validate time
    alarm_time = format_alarm_time(alarm_time)
    if not alarm_time:
        speak("Invalid time format. Please try again.")
        return

    # Store alarm time
    with open("Alarmtext.txt", "w") as time_file:
        time_file.write(alarm_time)

    speak(f"Alarm set successfully for {alarm_time}, sir.")

    # Run alarm.py as a background process
    subprocess.Popen(["python", "alarm.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)


import requests

def get_temperature(city=("karachi")):
    API_KEY = "829da55b8f7149ccb9e63907250404"
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"

    try:
        response = requests.get(url)
        data = response.json()

        # Debug: Print API response
        print("API Response:", data)  # Check the actual response from API

        if response.status_code == 200 and "current" in data:
            temp = data["current"].get("temp_c", "N/A")  # Get temperature in Celsius
            weather_desc = data["current"]["condition"]["text"]  # Weather description
            city_name = data["location"]["name"]
            country = data["location"]["country"]

            return f"Temperature in {city_name}, {country}: {temp}°C\nWeather: {weather_desc}"
        else:
            return f"Error: {data.get('error', {}).get('message', 'Unable to fetch weather data')}"
    except Exception as e:
        return f"Error: {e}"

# Test cases
cities = [
    "Karachi", "Lahore", "Faisalabad", "Rawalpindi", "Multan", "Gujranwala", "Peshawar", "Quetta", "Sialkot", "Sargodha",
    "Bahawalpur", "Sukkur", "Larkana", "Sheikhupura", "Jhang", "Dera Ghazi Khan", "Gujrat", "Mardan", "Kasur", "Rahim Yar Khan",
    "Sahiwal", "Okara", "Wah Cantonment", "Mingora", "Mirpur Khas", "Chiniot", "Nawabshah", "Kamoke", "Burewala", "Jhelum",
    "Sadiqabad", "Kohat", "Muridke", "Abottabad", "Pakpattan", "Khuzdar", "Vihari", "Gojra", "Mandi Bahauddin", "Tando Allahyar",
    "Daska", "Khanewal", "Dera Ismail Khan", "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Surat", "Pune", "Jaipur",
    "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam", "Pimpri-Chinchwad", "Patna", "Vadodara",
    "Ghaziabad", "Ludhiana", "Agra", "Nashik", "Faridabad", "Meerut", "Rajkot", "Kalyan-Dombivli", "Vasai-Virar", "Varanasi",
    "Srinagar", "Aurangabad", "Dhanbad", "Amritsar", "Navi Mumbai", "Allahabad","New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
    "Austin", "Jacksonville", "Fort Worth", "Columbus", "San Francisco", "Charlotte", "Indianapolis", "Seattle", "Denver", "Washington",
    "Boston", "El Paso", "Nashville", "Detroit", "London", "Turbat", "Muzaffargarh", "Bahawalnagar", "Shikarpur", "Charsadda", "Swabi", "Chaman"
]

for city in cities:
    print(f"print(get_temperature(\"{city}\")) # Fetch {city} weather")



from PyQt5.QtCore import Qt, QMetaObject, Q_ARG

def check_internet_speed():
    try:
        wifi = speedtest.Speedtest()
        wifi.get_best_server()

        speak("Testing download speed, please wait...")
        download_net = wifi.download() / 1048576  # Convert bytes to Megabits
        
        speak("Testing upload speed, please wait...")
        upload_net = wifi.upload() / 1048576  # Convert bytes to Megabits

        result = f"<font size=8 color='white'>Download: {download_net:.2f} Mbps | Upload: {upload_net:.2f} Mbps</font>"
        print(result)
        speak(f"Download speed: {download_net:.2f} Mbps, Upload speed: {upload_net:.2f} Mbps")

        # 🔵 Update GUI Label (Use main.label_internet_speed to update in the GUI thread)
        QMetaObject.invokeMethod(
            main.label_internet_speed, 
            "setText", 
            Qt.QueuedConnection, 
            Q_ARG(str, result)
        )

    except speedtest.ConfigRetrievalError:
        error_msg = "<font size=8 color='red'>Error: Server config failed.</font>"
        print("Failed to retrieve server configuration. Please check your connection.")
        speak("Failed to retrieve server configuration. Please check your connection.")
        QMetaObject.invokeMethod(main.label_internet_speed, "setText", Qt.QueuedConnection, Q_ARG(str, error_msg))

    except speedtest.SpeedtestException as e:
        error_msg = f"<font size=8 color='red'>Error: {str(e)}</font>"
        print("Speedtest error:", e)
        speak("Internet speed test failed. Please try again.")
        QMetaObject.invokeMethod(main.label_internet_speed, "setText", Qt.QueuedConnection, Q_ARG(str, error_msg))

    except Exception as e:
        error_msg = f"<font size=8 color='red'>Unexpected error: {str(e)}</font>"
        print("Unexpected error:", e)
        speak("An unexpected error occurred while checking internet speed.")
        QMetaObject.invokeMethod(main.label_internet_speed, "setText", Qt.QueuedConnection, Q_ARG(str, error_msg))


class mainT(QThread):
    def __init__(self):
        super(mainT, self).__init__()
    
    def run(self):
        while True:
            query = takeCommand()
            if "wake up" in query:
                speak("I am awake. How can I assist you?")
                self.execute_commands()
    
    def execute_commands(self):
        while True:
            query = takeCommand()
            if "good bye" in query or "finally sleep" in query:
                speak("Going to sleep, sir")
                break
            elif "pause" in query or "play" in query:
                    pyautogui.press("k")
            elif "mute" in query:
                    pyautogui.press("m")
            elif "volume up" in query:
                    from keyboard import volumeup
                    volumeup()
            elif "volume down" in query:
                    from keyboard import volumedown
                    volumedown()
            elif "remember that" in query:
                    rememberMessage = query.replace("remember that", "").strip()
                    with open("Reminder.txt", "a") as remember:
                        remember.write(rememberMessage + "\n")
                    speak("You told me to remember: " + rememberMessage)
            elif "what do you remember" in query:
                    with open("Reminder.txt", "r") as remember:
                        speak("You told me to " + remember.read())
            elif "tired" in query:
                    songs = [
                        "https://youtu.be/RmFUvp6GhiA?si=FNdW5qmKlM3rXCHl",
                        "https://youtu.be/XTp5jaRU3Ws?si=_QyBSTfVLAk6V4we",
                        "https://youtu.be/loTG-3F5kZ4?si=GUKAJjGrRAnBnph0"
                    ]
                    webbrowser.open(random.choice(songs))
            elif "news" in query or "latest news" in query:
                    latestnews()
            elif "calculate" in query:
                    from Calculatenumbers import Calc
                    Calc(query.replace("calculate", ""))

            elif "shutdown the system" in query:
                    speak("Are you sure you want to shut down?")
                    if input("Shutdown? (yes/no): ").lower() == "yes":
                        os.system("shutdown /s /t 1")
            elif "open google" in query:
                webbrowser.open("www.google.co.in")
                speak("Opening Google")
            elif "open youtube" in query:
                webbrowser.open("www.youtube.com")
                speak("Opening YouTube")
            elif "google" in query:
                from SearchNow import searchGoogle
                searchGoogle(query)
            elif "youtube" in query:
                from SearchNow import searchYoutube
                searchYoutube(query)
            elif "wikipedia" in query:
                from SearchNow import searchWikipedia
                searchWikipedia(query)
            elif "temperature in" in query:
                city = query.replace("temperature in", "").strip()
                weather_report = get_temperature(city)
                speak(weather_report)
                QMetaObject.invokeMethod(main.text_log, "append", Qt.QueuedConnection, Q_ARG(str, f"<b>Jarvis:</b> {weather_report}"))

            elif "temperature" in query or "weather" in query:
                weather_report = get_temperature()
                speak(weather_report)
                QMetaObject.invokeMethod(main.text_log, "append", Qt.QueuedConnection, Q_ARG(str, f"<b>Jarvis:</b> {weather_report}"))

            elif "tell me time" in query:
                speak(f"Sir, the time is {datetime.datetime.now().strftime('%I:%M %p')}")
            elif "internet speed" in query:
                check_internet_speed()
            elif "set an alarm" in query or "set alarm" in query :
                 set_alarm()      
            elif "whatsapp" in query:
                from Whatsapp import sendMessage
                sendMessage()
            elif "open" in query:
                from Dictapp import openappweb
                openappweb(query)
            elif "close" in query:
                from Dictapp import closeappweb
                closeappweb(query)

FROM_MAIN, _ = loadUiType(os.path.join(os.path.dirname(__file__), "./scifi.ui"))

class Main(QMainWindow, FROM_MAIN):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        # self.setFixedSize(1920, 1080)

        # Convert to absolute path
        # icon_path = os.path.abspath("./lib/exit-Copy.png").replace("\\", "/")

        # Check if file exists before applying style
        # if os.path.exists(icon_path):
        #     self.exitB.setStyleSheet(f"background-image: url({icon_path}); border:none;")
        # else:
        #     print(f"Error: Image file not found at {icon_path}")

        # self.exitB.clicked.connect(self.close)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)


        self.label_7 = QMovie("./lib/gifloader.gif", QByteArray(), self)
        self.label_7.setCacheMode(QMovie.CacheAll)
        self.label_4.setMovie(self.label_7)
        self.label_7.start()

        self.ts = time.strftime("%A, %d %B")
        self.label.setPixmap(QPixmap("./lib/tuse.png"))

        # Display Time
        self.label_5.setText(f"<font size=8 color='white'>{self.ts}</font>")
        self.label_5.setFont(QFont(QFont('Acens', 8)))

        # 🔹 Log Display for Speech and Commands
        self.text_log = QtWidgets.QTextEdit(self)
        self.text_log.setGeometry(600, 50, 800, 200)  # Adjust size and position as needed
        self.text_log.setReadOnly(True)
        self.text_log.setStyleSheet("background-color: black; color: white; font-size: 14px;")

        # 🔹 Label for Internet Speed (Styled on a Background Image)
        self.label_speed_background = QLabel(self)
        self.label_speed_background.setGeometry(50, 400, 400, 50)  # BELOW the time label

        self.minimizeB = QPushButton(self)
        self.minimizeB.setGeometry(1800, 10, 500, 500)  # Adjust position and size
        self.minimizeB.setText("_")  # You can also use an image
        self.minimizeB.setStyleSheet(
            "background-color: #222; color: white; font-size: 20px; border-radius: 10px;"
        )

        # 🔹 Connect to Minimize Function
        self.minimizeB.clicked.connect(self.showMinimized)

                # 🔹 Label for Speed Text (Displayed on Background)
        self.label_internet_speed = QLabel(self)
        self.label_internet_speed.setGeometry(50, 400, 400, 50)  # SAME position as background
        self.label_internet_speed.setFont(QFont('Acens', 8))
        self.label_internet_speed.setText("<font size=8 color='white'>Internet Speed: Waiting...</font>")
        self.label_internet_speed.setAlignment(Qt.AlignCenter)  # Centers text inside the label

        self.speak_thread = mainT()
        self.speak_thread.start()

    def update_log(self, text):
        """ Update GUI log with new text """
        self.text_log.append(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    exit(app.exec_())