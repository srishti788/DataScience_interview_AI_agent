import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

VALID_TOPICS = ["Python", "Sql", "Machine Learning", "Stats"]
VALID_DIFFICULTIES = ["Beginner", "Intermediate", "Advanced"]

MODEL_NAME = "gemini-2.5-flash"

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
    return response.text

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
    return response.text
print(" Welcome to the DATA SCIENCE INTERVIEW PREPARATION AGENT\n")

session = []

while True:
    # Get topic
    topic = input(f"Choose topic {VALID_TOPICS}: ").strip().title()
    if topic not in VALID_TOPICS:
        print("Invalid topic. Try again.")
        continue

    # Get difficulty
    difficulty = input(f"Choose difficulty {VALID_DIFFICULTIES}: ").strip().title()
    if difficulty not in VALID_DIFFICULTIES:
        print("Invalid difficulty. Try again.")
        continue

    # Generate and display question
    question = generate_question(topic, difficulty)
    print("\n Interview Question:")
    print(question)

    # Take answer
    answer = input("\n Your Answer:\n")

    # Evaluate answer
    feedback = evaluate_answer(question, answer)
    print("\n Feedback:")
    print(feedback)

    # Store in session
    session.append({
        "topic": topic,
        "difficulty": difficulty,
        "question": question,
        "answer": answer,
        "feedback": feedback
    })

    # Continue?
    cont = input("\nDo you want another question? (y/n): ").strip().lower()
    if cont != "y":
        print("\n Session Summary:")
        print(f"Total questions answered: {len(session)}")
        for i, q in enumerate(session, 1):
            print(f"{i}. Topic: {q['topic']} | Difficulty: {q['difficulty']}")
        print("\n Thank you for practicing! Keep learning!")
        break
