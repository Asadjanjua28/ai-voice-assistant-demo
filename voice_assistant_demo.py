import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import requests

engine = pyttsx3.init()
engine.setProperty('rate', 180)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def greet():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning.")
    elif hour < 18:
        speak("Good afternoon.")
    else:
        speak("Good evening.")
    speak("I am your assistant. How can I help you?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"You said: {query}")
        return query.lower()
    except:
        print("Sorry, I didn’t understand.")
        return ""

def get_weather(city, api_key="your_api_key_here"):
    try:
        url = f"http://api.weatherapi.com/v1/current.json"
        params = {"key": api_key, "q": city}
        response = requests.get(url, params=params)
        data = response.json()
        if "error" in data:
            return f"Couldn't find weather for {city}."
        curr = data["current"]
        return f"{city.title()} weather: {curr['condition']['text']}, {curr['temp_c']}°C."
    except:
        return "Weather service is not available."

def process_command(query):
    if "time" in query:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")

    elif "search for" in query:
        topic = query.replace("search for", "").strip()
        speak(f"Searching Wikipedia for {topic}")
        try:
            summary = wikipedia.summary(topic, sentences=2)
            speak(summary)
        except:
            speak("Couldn't find information.")

    elif "open youtube" in query:
        speak("Opening YouTube.")
        webbrowser.open("https://youtube.com")

    elif "weather" in query:
        city = query.split(" in ")[-1].strip() if " in " in query else "New York"
        speak(get_weather(city))

    elif any(word in query for word in ["exit", "quit", "stop"]):
        speak("Goodbye!")
        return False

    else:
        speak("Sorry, I can't help with that in the demo version.")
    return True

def main():
    greet()
    while True:
        query = take_command()
        if query:
            if not process_command(query):
                break

if __name__ == "__main__":
    main()
