import streamlit as st
import json
from PyPDF2 import PdfReader
from assistant import (
    record_audio, rms_of_wav, transcribe_audio, generate_answer, 
    get_motivational_response, detect_emotion_from_audio
)
from streamlit_TTS import text_to_speech

st.set_page_config(page_title="Accessible AI Voice Assistant", page_icon="🎤", layout="centered")

st.markdown("""
<div style="background-color:#4CAF50; padding: 30px; border-radius: 15px; margin-bottom: 25px;">
  <h1 style="text-align:center; color:#fff;">🎙️ EduAble </h1>
  <p style="text-align:center; color:#e0f2f1; font-size:18px;">
   A welcoming and inclusive learning space that provides good acoustics, clarity, contrast, and safety to facilitate independence and focus.  
</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Settings & Controls")
    language = st.selectbox("Select Language", ["English", "Hindi", "Tamil"])
    lang_map = {"English": "en-US", "Hindi": "hi-IN", "Tamil": "ta-IN"}
    voice_tone = st.selectbox("Voice Tone", ["Default", "Male", "Female"])
    speech_rate = st.slider("Voice Speed", 100, 250, 150)
    uploaded_file = st.file_uploader("Upload reference document (txt, json, pdf)", type=["txt", "json", "pdf"])
    use_ai_chat = st.checkbox("Use AI Chatbot (text input) instead of voice")

# Store quiz answers in session state
if 'quiz_questions' not in st.session_state:
    st.session_state['quiz_questions'] = []
if 'quiz_answers' not in st.session_state:
    st.session_state['quiz_answers'] = {}

doc_text = ""
if uploaded_file is not None:
    try:
        if uploaded_file.type == "application/pdf":
            pdf_reader = PdfReader(uploaded_file)
            doc_text = ""
            for page in pdf_reader.pages:
                doc_text += page.extract_text() + "\n"
        elif uploaded_file.type == "application/json":
            doc_data = json.load(uploaded_file)
            doc_text = json.dumps(doc_data)
        else:
            doc_text = uploaded_file.read().decode("utf-8")
        st.sidebar.success("Reference document loaded successfully!")
    except Exception:
        st.sidebar.error("Failed to read uploaded document!")

def show_emotion_status(emotion: str):
    emotion_colors = {
        "happy": "#00e676",
        "sad": "#ff5252",
        "neutral": "#ffd740",
        "frustrated": "#ffa726",
        "angry": "#d7263d"
    }
    st.markdown(f"""
    <div style="background-color:{emotion_colors.get(emotion, '#eee')}; 
    padding:15px; border-radius:10px; margin-bottom:10px;">
    <b>Emotion Status:</b> {emotion.capitalize()}
    </div>
    """, unsafe_allow_html=True)

def generate_quiz_and_explanation(prompt_text: str):
    # Append instruction to generate 10 questions plus answers
    prompt = prompt_text + "\nAfter explanation, include 10 short quiz questions with multiple-choice options and correct answers."
    return generate_answer(prompt)

def display_quiz_and_collect_answers():
    st.sidebar.header("Quiz Section")
    correct_count = 0
    total_questions = len(st.session_state['quiz_questions'])

    if total_questions == 0:
        st.sidebar.write("No quiz available yet.")
        return

    for i, q in enumerate(st.session_state['quiz_questions']):
        question_text = q.get('question', f"Question {i+1}")
        options = q.get('options', [])
        correct_answer = q.get('correct_answer', '')

        # Input key unique by question number
        user_answer = st.sidebar.radio(question_text, options, key=f"quiz_answer_{i}")

        st.session_state['quiz_answers'][f'q{i}'] = user_answer

        if user_answer == correct_answer:
            correct_count += 1

    if st.sidebar.button("Submit Quiz Answers"):
        st.sidebar.write(f"Your Score: {correct_count} / {total_questions}")
        if correct_count == total_questions:
            st.sidebar.success("Perfect score! Great job! 🎉")
            text_to_speech("Perfect score! Great job! Keep up the excellent work!", language=language.lower())
        elif correct_count >= total_questions * 0.7:
            st.sidebar.info("Good score! Keep practicing and you'll get even better.")
            text_to_speech("Good score! Keep practicing and you'll get even better.", language=language.lower())
        else:
            st.sidebar.warning("Keep trying! Practice makes perfect.")
            text_to_speech("Keep trying! Practice makes perfect. You can do it!", language=language.lower())

if use_ai_chat:
    st.subheader("AI Chatbot - Type your question/topic:")
    user_text = st.text_input("Enter your text here:")
    if st.button("Ask AI"):
        if not user_text.strip():
            st.warning("Please enter a question or topic!")
        else:
            base_prompt = f"Explain the topic: {user_text} clearly for a visually impaired student."
            if doc_text:
                if len(doc_text) > 2000:
                    truncated_doc = doc_text[:2000] + "\n...[truncated]"
                    base_prompt += f"\nReference document content:\n{truncated_doc}"
                else:
                    base_prompt += f"\nReference document content:\n{doc_text}"

            explanation_and_quiz = generate_quiz_and_explanation(base_prompt)
            st.markdown(f"""
            <div style="background-color:#e0f7fa; padding:20px; border-radius:15px; margin-top:20px;">
              <h3 style="color:#00796B;">🤖 Explanation & Quiz</h3>
              <pre style="font-size:18px; white-space: pre-wrap;">{explanation_and_quiz}</pre>
            </div>
            """, unsafe_allow_html=True)

            # Play spoken explanation and encouragement
            text_to_speech(explanation_and_quiz, language=language.lower())

            # Parse quiz questions from the answer (try-except for robustness)
            try:
                # Example: parsing JSON formatted quiz from AI if available; else use simple parse
                # Here assume quiz questions are in some structured format in explanation_and_quiz
                # For demo, create dummy quiz:
                st.session_state['quiz_questions'] = [
                    {
                        'question': f"Sample question {i+1}?",
                        'options': ['Option A', 'Option B', 'Option C', 'Option D'],
                        'correct_answer': 'Option A'
                    } for i in range(10)
                ]
            except Exception as e:
                st.warning("Could not parse quiz questions automatically.")
            
            display_quiz_and_collect_answers()
else:
    st.subheader("Voice Session - Click and speak your topic.")
    if st.button("Start Voice Session"):
        try:
            wav_file = record_audio(seconds=6)
            rms = rms_of_wav(wav_file)
            user_text = transcribe_audio(wav_file, lang=lang_map[language])
            emotion = detect_emotion_from_audio(wav_file)
            show_emotion_status(emotion)

            if not user_text:
                st.warning("Could not understand the audio. Please try again.")
            else:
                base_prompt = f"Explain the topic: {user_text} clearly for a visually impaired student."
                if doc_text:
                    if len(doc_text) > 2000:
                        truncated_doc = doc_text[:2000] + "\n...[truncated]"
                        base_prompt += f"\nReference document content:\n{truncated_doc}"
                    else:
                        base_prompt += f"\nReference document content:\n{doc_text}"
                base_prompt += "\nAfter explanation, include 10 short quiz questions with multiple-choice options and correct answers."
                if emotion in ["sad", "frustrated"] or rms < 0.01:
                    base_prompt += "\nInclude a motivational line at the end."

                explanation_and_quiz = generate_answer(base_prompt)
                final_output = explanation_and_quiz
                if (emotion in ["sad", "frustrated"] or rms < 0.01) and "motivat" not in explanation_and_quiz.lower():
                    final_output += f"\n\n{get_motivational_response()}"
                elif emotion == "happy":
                    cheer_message = "Great enthusiasm! Keep up the fantastic learning spirit!"
                    final_output += f"\n\n{cheer_message}"
                    
                st.markdown(f"""
                <div style="background-color:#e0f7fa; padding: 20px; border-radius: 15px; margin-top: 20px;">
                  <h3 style="color:#00796B;">🤖 Explanation & Quiz</h3>
                  <pre style="font-size: 18px; white-space: pre-wrap;">{final_output}</pre>
                </div>
                """, unsafe_allow_html=True)

                text_to_speech(final_output, language=language.lower())

                # For demo, generate dummy quiz as above
                st.session_state['quiz_questions'] = [
                    {
                        'question': f"Sample question {i+1}?",
                        'options': ['Option A', 'Option B', 'Option C', 'Option D'],
                        'correct_answer': 'Option A'
                    } for i in range(10)
                ]

                display_quiz_and_collect_answers()

                st.markdown("---")
                if st.button("Answer Quiz By Voice"):
                    ans_wav = record_audio(seconds=6)
                    ans_text = transcribe_audio(ans_wav, lang=lang_map[language])
                    st.success(f"Your answer captured: {ans_text}")

        except Exception as e:
            st.error(f"Unexpected error: {e}")

st.markdown("---")
st.markdown("""
<p style="text-align:center; color:#555; font-size:14px;">
Adjust language, voice tone, and speed via sidebar. Upload teaching materials for accessible explanations.<br>
Choose between AI chatbot text input or voice session.<br>
Emotional feedback and quizzes are delivered in every interaction.
</p>
""", unsafe_allow_html=True)
