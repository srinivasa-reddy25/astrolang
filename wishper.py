from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI  # Updated import
import uuid
import pyaudio
import wave
import os
from gtts import gTTS

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Updated initialization

# Audio recording settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5  # Adjust recording duration as needed
WAVE_OUTPUT_FILENAME = "input_audio.wav"

def record_audio():
    """Record audio from microphone"""
    p = pyaudio.PyAudio()
    
    print("Recording...")
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Recording finished.")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe_audio():
    """Transcribe audio using Whisper AI"""
    try:
        with open(WAVE_OUTPUT_FILENAME, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        print(f"Error in transcription: {e}")
        return None

def speak_response(text):
    """Convert text to speech"""
    try:
        tts = gTTS(text=text, lang="te")  # 'te' for Telugu
        tts.save("response.mp3")
        os.system("afplay response.mp3")  # For MacOS
        # For Windows use: os.system("start response.mp3")
        # For Linux use: os.system("mpg321 response.mp3")
    except Exception as e:
        print(f"Error in text-to-speech: {e}")

def main():
    # Initialize Firestore and Chat
    PROJECT_ID = "first-langchain"
    COLLECTION_NAME = "chat_history"
    SESSION_ID = str(uuid.uuid4())
    
    print("Start chatting with the AI. Say 'exit' to quit.")
    
    # Initialize Firestore Client
    client = firestore.Client(project=PROJECT_ID)
    
    # Initialize Chat History
    chat_history = FirestoreChatMessageHistory(
        session_id=SESSION_ID,
        collection=COLLECTION_NAME,
        client=client,
    )
    
    # Initialize ChatOpenAI
    llm = ChatOpenAI(model="gpt-4o-mini")
    
    # Define message template
    messages = [
        ("system", "You are CosmoGuru, a fun, engaging, and insightful Telugu-English AI assistant, "
                  "blending astrology with the festive spirit of Ugadi..."),
        ("human", "{query}")
    ]
    
    prompt_template = ChatPromptTemplate.from_messages(messages)
    
    while True:
        # Record audio
        print("Press Enter to start recording...")
        input()
        record_audio()
        
        # Transcribe audio
        query = transcribe_audio()
        if not query:
            print("Could not understand audio. Please try again.")
            continue
            
        print(f"You said: {query}")
        
        if query.lower() == "exit":
            print(f"Your Session ID for future reference: {SESSION_ID}")
            break
        
        # Process query and get AI response
        chat_history.add_user_message(query)
        formatted_prompt = prompt_template.invoke({"query": query})
        ai_response = llm.invoke(formatted_prompt)
        
        # Store and display AI response
        chat_history.add_ai_message(ai_response.content)
        print(f"AI: {ai_response.content}")
        
        # Convert AI response to speech
        speak_response(ai_response.content)
        
        # Cleanup temporary audio files
        if os.path.exists(WAVE_OUTPUT_FILENAME):
            os.remove(WAVE_OUTPUT_FILENAME)
        if os.path.exists("response.mp3"):
            os.remove("response.mp3")

if __name__ == "__main__":
    main()