
AI Voice Assistant — V0 (Prototype)
==================================

What this prototype does:
- Records a short audio clip from microphone (default 6 seconds).
- Sends audio to OpenAI Whisper (via OpenAI Python SDK) for transcription (STT).
- Sends text to OpenAI Chat (GPT) for answer generation (Q&A).
- Performs a simple "mood" check using audio volume (RMS). If below threshold, assistant appends a short motivational message.
- Speaks the final answer using pyttsx3 (TTS).
- Includes 2 sample quiz questions for demo.

Important prerequisites
-----------------------
1. Python 3.8+
2. Install packages: `pip install -r requirements.txt`
3. Set environment variable: OPENAI_API_KEY with your OpenAI API key.
   - Linux / macOS: `export OPENAI_API_KEY="sk-..."
   - Windows (PowerShell): `$env:OPENAI_API_KEY="sk-..."
4. A working microphone (default input device).

How to run
----------
1. Install requirements:
   pip install -r requirements.txt

2. (Optional) Edit quiz.json or sample_notes.txt to add your demo content.

3. Run the assistant:
   python app.py
   - The script records audio for 6 seconds by default. Speak your question clearly.
   - The app will transcribe, query GPT, perform volume-based mood check, and speak the answer.

Files in this package
---------------------
- app.py           : main runnable script
- assistant.py     : helper functions (recording, STT, GPT, mood detection, TTS)
- requirements.txt : pip dependencies
- quiz.json        : 2 sample quiz questions for demo
- sample_notes.txt : sample notes (phase 2 placeholder)
- README.md        : this file

Notes & caveats
----------------
- This is a minimal prototype for demo purposes.
- Whisper and GPT require an OpenAI API key and internet connectivity.
- If you prefer offline STT, replace the `transcribe_audio` function with a local STT solution (VOSK, Coqui STT, or local Whisper).
- The mood detection is intentionally simple (based on RMS volume) and only meant as a demo hook.
