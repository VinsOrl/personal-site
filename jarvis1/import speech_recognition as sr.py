import speech_recognition as sr
import pyttsx3
import openai

# 1. Setup your OpenAI API key (Get it from platform.openai.com)
openai.api_key = "YOUR_OPENAI_API_KEY_HERE"

# 2. Initialize Text-to-Speech Engine (Offline voice)
engine = pyttsx3.init()
# Set properties (Rate, Volume)
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

# Function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("J.A.R.V.I.S. is listening... (Say 'Jarvis' to start)")
        audio = r.listen(source)
    
    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        if "jarvis" in query.lower():
            return query
        return None
    except sr.UnknownValueError:
        speak("I didn't catch that.")
        return None
    except sr.RequestError:
        speak("Service is down.")
        return None

# Function to get AI response
def get_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant named J.A.R.V.I.S. Be polite, concise, and use British syntax."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Sorry, I'm having trouble connecting to the neural network."

# Main Loop
if __name__ == "__main__":
    speak("Hello. I am J.A.R.V.I.S. How can I assist you today?")
    
    while True:
        user_query = listen()
        if user_query and "jarvis" in user_query.lower():
            # Remove the wake word to get the actual command
            command = user_query.replace("jarvis", "").replace("jarvis", "").strip()
            
            if command:
                print(f"Processing: {command}")
                ai_reply = get_response(command)
                print(f"Reply: {ai_reply}")
                speak(ai_reply)
            else:
                speak("Yes, sir?")