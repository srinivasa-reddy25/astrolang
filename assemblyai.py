import assemblyai as aai
from elevenlabs import Voice, play, generate
from openai import OpenAI

class AI_Assistant:
    def __init__(self):
        # Initialize AssemblyAI client
        self.client = aai.Client(api_key="REDACTED_ASSEMBLYAI_KEY")
        
        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key="your-openai-key")
        
        # Initialize ElevenLabs
        self.elevenlabs_api_key = "your-elevenlabs-key"
        
        self.transcriber = None
        self.full_transcript = [
            {"role": "system", "content": "You are a receptionist at a dental clinic. Be resourceful and efficient."},
        ]

    def start_transcription(self):
        config = aai.TranscriberConfig(
            sample_rate=16000,
            on_data=self.on_data,
            on_error=self.on_error
        )
        
        self.transcriber = self.client.transcriber(config)
        self.transcriber.connect()
        
        microphone_stream = aai.extras.MicrophoneStream(
            sample_rate=16000
        )
        self.transcriber.stream(microphone_stream)

    # ... rest of your methods remain the same ...

    def generate_audio(self, text):
        self.full_transcript.append({"role": "assistant", "content": text})
        print(f"\nAI Receptionist: {text}")

        # Updated ElevenLabs audio generation
        audio = generate(
            text=text,
            voice="Rachel",
            model="eleven_monolingual_v1"
        )
        play(audio)

# Initialize and start the assistant
greeting = "Thank you for calling Vancouver dental clinic. My name is Sandy, how may I assist you?"
ai_assistant = AI_Assistant()
ai_assistant.generate_audio(greeting)
ai_assistant.start_transcription()