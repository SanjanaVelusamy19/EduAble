EduAble – AI Voice Assistant for Visually Impaired Students

EduAble is an intelligent, voice-driven educational assistant specially designed to empower visually impaired learners. Unlike traditional screen readers that only read text aloud, EduAble provides interactive learning, emotional support, natural conversation, and multi-modal assistance using advanced AI.

📝 Introduction

Visually impaired students face significant challenges in accessing standard study materials and learning independently. Most existing tools are limited to basic text-to-speech functionality and lack real-time interaction or emotional intelligence.

EduAble aims to solve these gaps by providing:

Interactive and adaptive learning support

Emotion-aware responses for motivation

Increased independence and engagement

Conversational AI assistance for academics and mental well-being

❗ Problem Statement
Problem Definition

Current accessibility tools for visually impaired learners primarily focus on reading text aloud, offering minimal interaction and support.

Need for a Solution

No real-time conversational interaction

No emotional awareness or adaptive motivation

Limited engagement during self-learning

Gap in Existing Systems

These limitations cause:

Reduced independence

Lower motivation

Frustration and poor learning engagement

✅ Proposed System

EduAble integrates AI, speech recognition, emotion detection, and natural language processing into one unified assistant.

Key Features & Innovations

📖 Reads PDFs and notes aloud (automatic text extraction)

🎤 Understands spoken questions using SpeechRecognition

🤖 Answers academic queries using OpenAI GPT

❤️ Detects user emotions through voice (Hugging Face API)

🗣️ Gives motivational, emotion-aware responses

🌍 Multi-lingual voice support

⚙️ Adjustable speech speed and pitch

🔄 Workflow
1. Data Collection

PDFs, notes, and sample academic queries

Voice samples for emotion detection

2. Preprocessing

Extract text from PDFs

Clean and normalize text

Prepare voice samples for analysis

3. Core Module Development

Speech Recognition: SpeechRecognition library

Text-to-Speech: gTTS

Emotion Detection: Hugging Face API

AI Question Answering: OpenAI GPT

PDF Processing: PyPDF2

Audio Handling: Pydub, Soundfile

4. Integration

All modules integrated into a simple and accessible Streamlit web app with voice buttons and clean UI.

5. Testing & Validation

Voice command accuracy

Emotional detection reliability

User experience feedback from visually impaired learners

🛠 Tech Stack
Component	Technology	Purpose
Language	Python	Core backend logic
UI Framework	Streamlit	Simple, accessible web interface
Speech Recognition	SpeechRecognition	Converts speech → text
Text-to-Speech	gTTS	Converts text → voice
Emotion Detection	Hugging Face API	Analyzes user emotions
AI Engine	OpenAI GPT	Q&A, explanations, conversation
PDF Processing	PyPDF2	Text extraction
Audio Support	Pydub, Soundfile	Handling and converting audio
📁 Project Structure
EduAble/
│── app.py                     # Main Streamlit application  
│── speech_to_text.py          # Speech recognition module  
│── text_to_speech.py          # gTTS voice output  
│── emotion_detection.py       # Hugging Face API for emotions  
│── ai_engine.py               # OpenAI GPT logic  
│── pdf_reader.py              # PDF text extraction  
│── requirements.txt           # Dependencies  
│── assets/                    # Audio icons, images, samples  
│── .env                       # API keys (excluded from repo)  

▶️ How to Run
1. Clone the Repository
git clone https://github.com/SanjanaVelusamy19/EduAble.git
cd EduAble

2. Create Virtual Environment
python -m venv venv
venv/Scripts/activate

3. Install Dependencies
pip install -r requirements.txt

4. Add API Keys

Create a .env file:

OPENAI_API_KEY=your_key_here
HUGGINGFACE_API_KEY=your_key_here

5. Run the App
streamlit run app.py

🌟 Future Enhancements

Offline voice processing

Real-time classroom assistant

Personalized study plans

Emotion-based learning difficulty adjustment

Braille device integration

Adaptive quizzes & performance dashboard

👩‍💻 Developer

Sanjana V
Creator & Developer of EduAble
