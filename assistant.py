import os
import json
import numpy as np
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from groq import Groq
from dotenv import load_dotenv
from gtts import gTTS
from transformers import pipeline
import tempfile
import base64

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
emotion_pipeline = pipeline("audio-classification", model="superb/wav2vec2-base-superb-er")

def record_audio(filename="recorded.wav", samplerate=16000, channels=1, seconds=6):
    recording = sd.rec(int(seconds * samplerate), samplerate=samplerate, channels=channels, dtype='int16')
    sd.wait()
    sf.write(filename, recording, samplerate)
    return filename

def rms_of_wav(filename):
    data, sr = sf.read(filename, dtype='float32')
    if data.ndim > 1:
        data = data.mean(axis=1)
    rms = np.sqrt(np.mean(np.square(data)))
    return float(rms)

def transcribe_audio(filename, lang="en-US"):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language=lang)
    except Exception:
        return ""

def generate_answer(prompt):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("Groq request failed:", e)
        return "Sorry, I couldn't get an answer."

def get_motivational_response():
    return "Hey — I noticed you might be feeling low. You’re doing great; keep going, one step at a time."

def detect_emotion_from_audio(filename):
    try:
        results = emotion_pipeline(filename)
        top_emotion = max(results, key=lambda x: x['score'])
        return top_emotion['label']
    except Exception:
        return "neutral"

def speak_text_streamlit(text, lang):
    try:
        tts = gTTS(text=text, lang=lang.split('-')[0])
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        b64_audio = base64.b64encode(mp3_fp.read()).decode('utf-8')
        audio_html = f"""
        <audio autoplay controls>
            <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3" />
            Your browser does not support the audio element.
        </audio>
        """
        return audio_html
    except Exception as e:
        print(f"gTTS error: {e}")
        return None