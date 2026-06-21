import os
from groq import Groq
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.rag import search_documents

router = APIRouter(tags=["chat"])
conversation_history = []

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an intelligent AI assistant for a Knowledge Management System.
You help users find information, summarize documents, answer questions clearly and professionally.
Use the provided document context when relevant, and say so if you used it.
Format responses with clear structure using headings and bullet points where useful."""

QUICK_PROMPTS = {
    "Summarize the uploaded documents": "Provide a professional summary including main topics, key points, and important findings. Format with clear headings.",
    "key topics": "List the key topics and themes as a numbered list with brief explanations for each.",
    "professional summary report": "Generate a professional executive summary report:\n1. Overview\n2. Key Findings\n3. Main Topics\n4. Recommendations",
    "questions should I ask": "Suggest 10 insightful questions organized by: Understanding, Analysis, and Action items."
}


class ChatRequest(BaseModel):
    question: str
    clear_history: bool = False


@router.post("/chat")
async def chat(request: ChatRequest):
    global conversation_history

    if request.clear_history:
        conversation_history = []
        return {"answer": "Conversation cleared."}

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    if not os.getenv("GROQ_API_KEY"):
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not found in .env")

    question = request.question
    for trigger, prompt in QUICK_PROMPTS.items():
        if trigger in question:
            question = prompt
            break

    try:
        chunks = search_documents(question, k=4)
    except Exception:
        chunks = []

    used_rag = bool(chunks)
    user_message = question
    if chunks:
        user_message += "\n\nRelevant document excerpts:\n" + "\n---\n".join(chunks)

    conversation_history.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history,
            max_tokens=1024
        )

        answer = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": answer})

        return {
            "answer": answer,
            "history_length": len(conversation_history),
            "used_rag": used_rag
        }

    except Exception as e:
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