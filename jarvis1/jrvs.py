import speech_recognition as sr
import pyttsx3
import ollama
import time
import os

# --- 1. Setup Ollama Connection ---
# Make sure this is exactly what you want to use
OLLAMA_HOST = "http://127.0.0.1:11434"
print(f"[DEBUG] Using OLLAMA_HOST = {OLLAMA_HOST}")

client = ollama.Client(host=OLLAMA_HOST)

# --- 2. Setup Voice Engine ---
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def speak(text):
    print(f"[J.A.R.V.I.S.]: {text}")
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.8)

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("J.A.R.V.I.S. listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source, timeout=10)

    try:
        query = r.recognize_google(audio, language='en-in').lower()
        print(f"User: {query}")
        return query
    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        speak("I didn't catch that.")
        return None
    except sr.RequestError:
        speak("Connection to speech server failed.")
        return None

# --- 3. AI Brain (Using Ollama) ---
def ask_ollama(user_input):
    try:
        response = client.chat(
            model='gemma4:31b',  # Use the actual model name from your curl output
            messages=[{
                'role': 'user',
                'content': user_input,
            }],
        )
        return response['message']['content']
    except Exception as e:
        return f"Error communicating with Ollama: {e}"

# --- 4. Main Loop ---
def main():
    speak("Hello. I am J.A.R.V.I.S. ready to assist you.")
    
    while True:
        user_query = listen()
        
        if user_query:
            # Check for specific commands
            if "exit" in user_query or "quit" in user_query:
                speak("Goodbye.")
                break
            
            # Check if the user addressed the AI
            elif "jarvis" in user_query or "jarvis" in user_query:
                # Clean the command (remove the word 'jarvis')
                clean_query = user_query.replace("jarvis", "").replace("jarvis", "").strip()
                if clean_query:
                    print(f"Processing: {clean_query}")
                    reply = ask_ollama(clean_query)
                    print(f"Response: {reply}")
                    speak(reply)
                else:
                    speak("Yes, sir?")
            else:
                # If no "jarvis" command, treat as normal query
                print(f"Processing: {user_query}")
                reply = ask_ollama(user_query)
                print(f"Response: {reply}")
                speak(reply)

if __name__ == "__main__":
    # Test connection first
    try:
        print("Testing Ollama connection...")
        models = client.list()
        print("Connection successful!")
        print(f"Available models: {[m['model'] for m in models['models']]}")
    except Exception as e:
        print(f"Connection test failed: {e}")
        speak("I couldn't reach the Ollama server. Please start it first.")
        os._exit(0)

    main()