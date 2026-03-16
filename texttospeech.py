from gtts import gTTS
import os

def speak_text(text):
    tts = gTTS(text=text, lang="te")  # 'te' for Telugu, 'en' for English
    tts.save("response.mp3")
    os.system("afplay response.mp3")  # Use 'afplay' on MacOS

# Example usage
speak_text("Ugadi Subhakankshalu! Mee kutumbam andariki ee samvatsaram anandamga undali.")






