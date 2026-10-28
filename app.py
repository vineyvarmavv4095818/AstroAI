
import os
from dotenv import load_dotenv
from google import genai
import requests
import numpy as np

load_dotenv()

OLLAMA_MODEL = "gemma3:1b"

SYSTEM_PROMPT = """
You are AstroAI, a friendly astronomy tutor.

Instructions:
- Explain concepts in simple English.
- Assume the user is a beginner.
- Keep each answer under 100 words.
- Give an example when helpful.
- Use previous messages to understand follow-up questions.
- If the user says "it", "they", or "that", use conversation
  context to understand what they mean.
"""


def ask_ollama(question, history=None):
    if not question or not question.strip():
        return "Please ask a valid question."

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # Add previous conversation
    if history:
        for message in history:
            if message["role"] in ("user", "assistant"):
                messages.append({
                    "role": message["role"],
                    "content": message["content"]
                })

    # Add current question
    messages.append({
        "role": "user",
        "content": question
    })

    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": messages,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()
        data = response.json()

        return data["message"]["content"]

    except requests.exceptions.RequestException as e:
        return f"Ollama connection error: {e}"

    except (KeyError, ValueError) as e:
        return f"Ollama response error: {e}"





def get_embedding(text):
    """Convert text into an embedding vector using Ollama."""
    response = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "nomic-embed-text",
            "input": text
        },
        timeout=120
    )

    response.raise_for_status()
    return response.json()["embeddings"][0]


def cosine_similarity(a, b):
    """Calculate similarity between two embedding vectors."""
    a = np.array(a)
    b = np.array(b)

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return 0.0

    return float(np.dot(a, b) / denominator)


def ask_knowledge(question):
    """Answer a question using AstroAI's local space knowledge."""

    if not question or not question.strip():
        return "Please ask a valid question."

    # Read the knowledge file
    try:
        with open(
            "space_knowledge.txt",
            "r",
            encoding="utf-8"
        ) as file:
            knowledge = file.read()

    except OSError:
        return "Could not find space_knowledge.txt."

    # Split the knowledge into sections
    sections = [
        section.strip()
        for section in knowledge.split("## ")
        if section.strip()
    ]

    if not sections:
        return "The knowledge file is empty."

    try:
        # Create embeddings for each section
        section_embeddings = [
            get_embedding(section)
            for section in sections
        ]

        # Embed the user's question
        question_embedding = get_embedding(question)

        # Find the best matching section
        scores = [
            (
                cosine_similarity(question_embedding, embedding),
                section
            )
            for section, embedding
            in zip(sections, section_embeddings)
        ]

        best_score, best_section = max(
            scores,
            key=lambda item: item[0]
        )

        # Reject weak matches
        if best_score < 0.65:
            return (
                "I couldn't find sufficiently relevant information "
                "in my space knowledge file."
            )

        # Generate an answer using the retrieved information
        prompt = f"""
You are AstroAI, a friendly astronomy tutor.

Answer the question using only the knowledge below.
Use simple English and keep your answer under 100 words.
If the knowledge does not contain the answer, say so.
Do not invent facts.

Knowledge:
{best_section}

Question:
{question}
"""

        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()
        return response.json()["message"]["content"]

    except requests.exceptions.RequestException as e:
        return f"RAG connection error: {e}"

    except (KeyError, ValueError) as e:
        return f"RAG response error: {e}"


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing in .env file.")

client = genai.Client(api_key=api_key)


def ask_gemini(question, history=None):
    if not question or not question.strip():
        return "Please ask a valid question."

    # Build conversation context for Gemini
    conversation = []

    if history:
        for message in history:
            if message["role"] == "user":
                conversation.append(
                    f"User: {message['content']}"
                )
            elif message["role"] == "assistant":
                conversation.append(
                    f"AstroAI: {message['content']}"
                )

    conversation.append(f"User: {question}")

    prompt = (
        SYSTEM_PROMPT
        + "\n\nConversation so far:\n"
        + "\n".join(conversation)
        + "\n\nReply to the latest user message as AstroAI."
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text or "No text response received."

    except Exception as e:
        return f"Gemini error: {e}"


if __name__ == "__main__":
    question = input("Ask an astronomy question: ")

    print("\n--- Gemini Answer ---")
    print(ask_gemini(question))

    print("\n--- Ollama Answer ---")
    print(ask_ollama(question))
