import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

def get_voice_input():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand. Try again.")
        return None
    except sr.RequestError:
        print("Could not request results, check internet connection.")
        return None

# Call function to capture voice input
user_input = get_voice_input()
