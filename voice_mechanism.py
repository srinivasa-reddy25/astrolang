from TTS.api import TTS
import sounddevice as sd
import soundfile as sf
import numpy as np
import wave
import webrtcvad
import os
from vosk import Model, KaldiRecognizer

class VoiceMechanism:
    def __init__(self):
        # Initialize TTS
        self.tts = TTS(model_name="tts_models/tel/tel_unified/vits")  # Telugu model
        
        # Audio recording parameters
        self.sample_rate = 16000
        self.channels = 1
        self.frame_duration = 30  # ms
        
        # VAD (Voice Activity Detection) setup
        self.vad = webrtcvad.Vad(3)
        
        # Initialize Vosk model for speech recognition
        self.speech_model = Model(lang="en")  # Make sure to download the model first

    def record_audio(self, duration=5):
        """Record audio with voice activity detection"""
        print("Recording... (Speak now)")
        
        frames = []
        silence_threshold = 0.02
        silence_counter = 0
        max_silence_frames = int(self.sample_rate * 1.5)  # 1.5 seconds of silence
        
        def callback(indata, frames, time, status):
            if status:
                print(status)
            frames.extend(indata.copy())
            
            # Check for silence
            if np.abs(indata).mean() < silence_threshold:
                nonlocal silence_counter
                silence_counter += len(indata)
            else:
                silence_counter = 0
        
        with sd.InputStream(samplerate=self.sample_rate, channels=self.channels, 
                          callback=callback):
            while silence_counter < max_silence_frames:
                sd.sleep(100)
        
        return np.array(frames)

    def save_audio(self, audio_data, filename="input.wav"):
        """Save audio data to file"""
        sf.write(filename, audio_data, self.sample_rate)
        return filename

    def transcribe_audio(self, audio_file):
        """Transcribe audio using Vosk"""
        try:
            with wave.open(audio_file, "rb") as wf:
                rec = KaldiRecognizer(self.speech_model, wf.getframerate())
                
                while True:
                    data = wf.readframes(4000)
                    if len(data) == 0:
                        break
                    if rec.AcceptWaveform(data):
                        continue
                
                result = rec.FinalResult()
                return result.get("text", "")
        except Exception as e:
            print(f"Error in transcription: {e}")
            return None

    def speak(self, text):
        """Convert text to speech using Coqui TTS"""
        try:
            # Generate speech
            wav_file = "response.wav"
            self.tts.tts_to_file(text=text, file_path=wav_file)
            
            # Play audio
            data, sr = sf.read(wav_file)
            sd.play(data, sr)
            sd.wait()
            
            # Cleanup
            os.remove(wav_file)
            
        except Exception as e:
            print(f"Error in text-to-speech: {e}")

    def get_voice_input(self):
        """Complete process to get voice input and convert to text"""
        audio_data = self.record_audio()
        audio_file = self.save_audio(audio_data)
        text = self.transcribe_audio(audio_file)
        os.remove(audio_file)  # Cleanup
        return text

    def cleanup(self):
        """Cleanup any temporary files"""
        for file in ["input.wav", "response.wav"]:
            if os.path.exists(file):
                os.remove(file)