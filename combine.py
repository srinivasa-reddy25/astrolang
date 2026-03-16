import speech_recognition as sr
from gtts import gTTS
import os
# Initialize recognizer

recognizer = sr.Recognizer()

def get_voice_input():
    """Captures user voice input and converts it to text."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        print("User said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand. Try again.")
        return None
    except sr.RequestError:
        print("Could not request results, check internet connection.")
        return None

def speak_text(text):
    """Converts AI's text response to speech and plays it."""
    tts = gTTS(text=text, lang="te")  # Telugu voice
    tts.save("response.mp3")
    os.system("afplay response.mp3")  # Use 'afplay' on MacOS

# Get user query (Speech-to-Text)
# user_query = get_voice_input()

# if user_query:
    
    # TODO: Replace this with AI-generated response
    # ai_response = "Mee prashna ki samadhanam: Ugadi ante kotta aasha mariyu prarambham."  # Placeholder AI response
    # ai_response=main.
    # Speak AI response (Text-to-Speech)
    # speak_text(ai_response)

def process_ai_result(result: str):
    # Process the AI result here
    # Add your logic to handle the result
    ai_response = result
    speak_text(ai_response)
        
        # return result  # or return processed result
    
