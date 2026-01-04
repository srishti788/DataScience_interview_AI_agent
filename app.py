import os
from dotenv import load_dotenv
import streamlit as st
from google import genai

# Load environment variables
load_dotenv()

# Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL_NAME = "gemini-2.5-flash"

VALID_TOPICS = ["Python", "SQL", "Machine Learning", "Stats"]
VALID_DIFFICULTIES = ["Beginner", "Intermediate", "Advanced"]

# -------------------------------
# AI FUNCTIONS
# -------------------------------
def generate_question(topic, difficulty):
    prompt = f"""
    You are a Data Science interviewer.
    Ask ONE {difficulty} level interview question on {topic}.
    Keep it concise.
    """
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text.strip()

def evaluate_answer(question, answer):
    prompt = f"""
    You are evaluating a Data Science interview answer.

    Question:
    {question}

    Candidate Answer:
    {answer}

    Provide:
    1. Score out of 10
    2. Missing or weak concepts
    3. Correct improved answer (short)
    """
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    return response.text.strip()

# -------------------------------
# STREAMLIT UI
# -------------------------------
st.set_page_config(page_title="AI Interview Preparation Agent", layout="centered")

st.title("🤖 AI Interview Preparation Agent")
st.caption("IBM SkillsBuild | Applied AI | Final Project")

# Session state
if "session" not in st.session_state:
    st.session_state.session = []
if "question" not in st.session_state:
    st.session_state.question = None

# Topic & Difficulty
topic = st.selectbox("Choose Topic", VALID_TOPICS)
difficulty = st.selectbox("Choose Difficulty", VALID_DIFFICULTIES)

# Generate Question
if st.button("🎯 Generate Question"):
    st.session_state.question = generate_question(topic, difficulty)

# Display Question
if st.session_state.question:
    st.subheader("🧠 Interview Question")
    st.write(st.session_state.question)

    answer = st.text_area("✍️ Your Answer", height=150)

    if st.button("📊 Evaluate Answer"):
        if answer.strip() == "":
            st.warning("Please write an answer first.")
        else:
            feedback = evaluate_answer(st.session_state.question, answer)

            st.subheader("✅ Feedback")
            st.write(feedback)

            # Save session
            st.session_state.session.append({
                "topic": topic,
                "difficulty": difficulty,
                "question": st.session_state.question
            })

# Session Summary
if st.session_state.session:
    st.divider()
    st.subheader("📘 Session Summary")
    st.write(f"Total Questions Answered: {len(st.session_state.session)}")

    for i, s in enumerate(st.session_state.session, 1):
        st.write(f"{i}. {s['topic']} | {s['difficulty']}")

