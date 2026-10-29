
import requests

# Step 1: Read our knowledge file
with open("space_knowledge.txt", "r", encoding="utf-8") as file:
    knowledge = file.read()

# Step 2: Get the user's question
question = input("Ask a space question: ")

# Step 3: Find relevant sections
sections = knowledge.split("## ")
question_words = set(question.lower().split())
stop_words = {"the", "is", "a", "an", "about", "tell", "me", "what", "who", "how", "does", "explain"}

keywords = question_words - stop_words
matches = []

for section in sections:
    if not section.strip():
        continue

    section_words = set(section.lower().split())

    if any(word.strip(".,?!") in section_words for word in keywords):
        matches.append(section.strip())

# Step 4: Prepare context for the AI
if not matches:
    print("No relevant information found in the knowledge file.")

else:
    context = "\n\n".join(matches)

    prompt = f"""
Answer the question using the knowledge provided below.
If the answer is not in the knowledge, clearly say so.
Do not invent facts.

Knowledge:
{context}

Question: {question}
"""

    # Step 5: Ask Ollama
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "gemma3:1b",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()
    answer = response.json()["message"]["content"]

    print("\nCosmoAI Answer:")
    print(answer)
