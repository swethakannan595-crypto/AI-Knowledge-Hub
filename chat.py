import os
from groq import Groq
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag import search_documents_with_scores

router = APIRouter(tags=["chat"])
conversation_history = []

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an intelligent AI assistant for a Knowledge Management System called Index.

Your behavior rules:
1. If [Document Context] is provided below the question — use it to answer. Mention which document the info came from if helpful.
2. If NO [Document Context] is provided — answer from your own general knowledge. Never say "the document doesn't contain this". Just answer helpfully.
3. NEVER refuse to answer. Always give a useful response.
4. Be professional, clear, and concise.
5. Format responses with headings and bullet points where it helps readability."""

QUICK_PROMPTS = {
    "Summarize the uploaded documents": "Please provide a professional summary of the uploaded documents. Include main topics, key points, and important findings with clear headings.",
    "What are the key topics in my documents?": "List all key topics and themes found in the uploaded documents as a numbered list with brief explanations for each.",
    "Give me a professional summary report": "Generate a professional executive summary report including: 1. Overview  2. Key Findings  3. Main Topics  4. Recommendations",
    "What questions should I ask about this content?": "Based on the uploaded documents, suggest 10 insightful questions organized by category: Understanding, Analysis, and Action items."
}

# Relevance threshold for RAG
# ChromaDB cosine distance: 0.0 = identical, 2.0 = completely opposite
# Below 0.75 = genuinely relevant to the question
# Above 0.75 = not relevant enough — skip and use general knowledge
RELEVANCE_THRESHOLD = 0.75


class ChatRequest(BaseModel):
    question: str
    clear_history: bool = False


@router.post("/chat")
async def chat(request: ChatRequest):
    global conversation_history

    if request.clear_history:
        conversation_history = []
        return {"answer": "Chat cleared. Upload a PDF and ask me anything about it.", "used_rag": False}

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    if not os.getenv("GROQ_API_KEY"):
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not found in .env file")

    # Check quick prompt triggers
    question = request.question
    for trigger, prompt in QUICK_PROMPTS.items():
        if trigger in question:
            question = prompt
            break

    # Smart RAG — only use chunks that are genuinely relevant
    relevant_chunks = []
    used_rag = False
    source_files = set()

    try:
        results = search_documents_with_scores(question, k=5)

        for chunk, distance in results:
            if distance < RELEVANCE_THRESHOLD and chunk and len(chunk.strip()) > 20:
                relevant_chunks.append(chunk)

        used_rag = bool(relevant_chunks)
        print(f"RAG: {len(relevant_chunks)} relevant chunks found (threshold={RELEVANCE_THRESHOLD})")

    except Exception as e:
        print(f"RAG error: {e}")
        relevant_chunks = []
        used_rag = False

    # Build user message — only attach context if relevant chunks found
    if relevant_chunks:
        context = "\n---\n".join(relevant_chunks)
        user_message = f"""{question}

[Document Context — answer using this if relevant:]
{context}"""
    else:
        # No relevant document context — answer from general knowledge
        user_message = question

    conversation_history.append({"role": "user", "content": user_message})

    # Keep history to last 20 messages to avoid token overflow
    if len(conversation_history) > 20:
        conversation_history = conversation_history[-20:]

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history,
            max_tokens=1024,
            temperature=0.7
        )

        answer = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": answer})

        return {
            "answer": answer,
            "used_rag": used_rag,
            "history_length": len(conversation_history)
        }

    except Exception as e:
        # Remove the failed message from history
        if conversation_history:
            conversation_history.pop()
        raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")


@router.get("/chat/history")
async def get_history():
    return {"history": conversation_history}


@router.delete("/chat/history")
async def clear_history():
    global conversation_history
    conversation_history = []
    return {"message": "History cleared"}
