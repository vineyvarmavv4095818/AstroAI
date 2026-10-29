
import requests
import numpy as np

# 1. Generate embeddings using Ollama
def get_embedding(text):
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


# 2. Calculate cosine similarity
def similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


# 3. Read the knowledge file
with open("space_knowledge.txt", "r", encoding="utf-8") as file:
    knowledge = file.read()

# 4. Divide knowledge into sections
sections = [
    section.strip()
    for section in knowledge.split("## ")
    if section.strip()
]

# 5. Generate an embedding for each section
section_embeddings = []

for section in sections:
    embedding = get_embedding(section)
    section_embeddings.append(embedding)

print(f"Loaded {len(sections)} knowledge sections.")

# 6. Ask a question
question = input("\nAsk a space question: ")

# 7. Generate the question embedding
question_embedding = get_embedding(question)

# 8. Find the most relevant section
scores = []

for section, embedding in zip(sections, section_embeddings):
    score = similarity(question_embedding, embedding)
    scores.append((score, section))

scores.sort(key=lambda item: item[0], reverse=True)



# 9. Retrieve relevant information and ask Ollama
best_score, best_section = scores[0]

THRESHOLD = 0.65

print(f"\nBest similarity score: {best_score:.3f}")

if best_score < THRESHOLD:
    print("\nCosmoAI: Sorry, I couldn't find sufficiently relevant information in my knowledge file.")

else:
    print("\nRetrieved information:")
    print(best_section)

    prompt = f"""
You are CosmoAI, a helpful space assistant.

Answer the user's question using only the knowledge below.
If the information does not contain the answer, say that you don't
have enough information. Do not invent facts.
Explain the answer in simple English.

Knowledge:
{best_section}

User question:
{question}
"""

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": "gemma3:1b",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()
    answer = response.json()["message"]["content"]

    print("\nCosmoAI Answer:")
    print(answer)


