import pyttsx3
import datetime
import os
import time

# Initialize the TTS engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 200)

def speak(audio):
    """Function to make Jarvis speak"""
    print(f"Speaking: {audio}")  # Debugging output
    engine.say(audio)
    engine.runAndWait()

# Ensure the alarm file exists before opening
alarm_file = "Alarmtext.txt"

if not os.path.exists(alarm_file):
    speak("Alarm file not found. Please set the alarm again.")
    print("Error: Alarm file not found.")
    exit()

# Read the alarm time from the file
with open(alarm_file, "rt") as file:
    alarm_time = file.read().strip()  # Read and remove extra spaces/newlines

if not alarm_time:
    speak("Alarm file is empty. Please set the alarm again.")
    print("Error: Alarm file is empty.")
    exit()

print(f"Alarm time from file: {alarm_time}")  # Debugging output

# Clear the file after reading
with open(alarm_file, "w") as file:
    file.truncate(0)

def convert_to_24hr(alarm_time):
    """Convert 12-hour AM/PM format to 24-hour format, or validate 24-hour format."""
    try:
        return datetime.datetime.strptime(alarm_time, "%I:%M %p").strftime("%H:%M")
    except ValueError:
        try:
            return datetime.datetime.strptime(alarm_time, "%H:%M").strftime("%H:%M")  # Already in 24-hour format
        except ValueError:
            return None

def ring(alarm_time_24):
    """Function to check and ring alarm"""
    print(f"Alarm set for {alarm_time_24}")
    
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")  # Format: HH:MM
        print(f"Current time: {current_time}, Waiting for: {alarm_time_24}")  # Debugging output
        
        if current_time == alarm_time_24:
            speak("Alarm ringing, sir.")
            
            # Play the music file
            music_path = r"C:\\Users\\hp\\Desktop\\JARVIS\\music.mp3"
            
            if os.path.exists(music_path):
                os.startfile(music_path)
            else:
                speak("Music file not found. Please check the path.")
                print("Error: Music file not found.")

            break  # Exit the loop once the alarm rings

        time.sleep(5)  # Reduced sleep time for quicker debugging

# Convert alarm_time to 24-hour format before proceeding
alarm_time_24 = convert_to_24hr(alarm_time)

if alarm_time_24:
    ring(alarm_time_24)
else:
    print("Invalid time format. Please enter time in HH:MM AM/PM or 24-hour format.")
    speak("Invalid time format. Please set the alarm again.")
