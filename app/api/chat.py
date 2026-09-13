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

1. If [Document Context] is provided below the question, use that context to answer.
2. When document context is provided, base the answer primarily on the uploaded document content.
3. If multiple document chunks are provided, combine them to produce a useful overall answer.
4. If NO document context is provided, answer from your own general knowledge.
5. Never say "the document doesn't contain this" unless document context was actually provided and the information is genuinely absent.
6. NEVER refuse to answer. Always provide a useful response.
7. Be professional, clear, and concise.
8. For summaries, summarize the actual document content instead of giving a generic template.
9. For quick document actions, use all relevant document chunks supplied in the context.
10. Format responses with headings and bullet points where helpful.
"""

QUICK_PROMPTS = {
    "Summarize the uploaded documents":
        "Summarize the uploaded document content provided below. Identify the main topics, important points, key findings, and conclusions. Do not give a generic summary template. Summarize the actual content.",

    "What are the key topics in my documents?":
        "Identify the key topics and themes from the uploaded document content provided below. Give a numbered list with a short explanation for each topic.",

    "Give me a professional summary report":
        "Create a professional summary report from the uploaded document content provided below. Include Overview, Key Findings, Main Topics, and Recommendations based only on the provided document content.",

    "What questions should I ask about this content?":
        "Based on the uploaded document content provided below, suggest 10 useful questions. Organize them into Understanding, Analysis, and Action Items."
}

RELEVANCE_THRESHOLD = 0.75


class ChatRequest(BaseModel):
    question: str
    clear_history: bool = False


@router.post("/chat")
async def chat(request: ChatRequest):

    global conversation_history

    if request.clear_history:
        conversation_history = []

        return {
            "answer": "Chat cleared. Upload a PDF and ask me anything about it.",
            "used_rag": False
        }

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    if not os.getenv("GROQ_API_KEY"):
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY not found"
        )

    original_question = request.question
    question = original_question

    # Detect quick document actions
    is_quick_action = False

    for trigger, prompt in QUICK_PROMPTS.items():
        if trigger.lower() in question.lower():
            question = prompt
            is_quick_action = True
            break

    relevant_chunks = []
    used_rag = False

    try:

        # IMPORTANT:
        # Do NOT use get_all_documents().
        # It can load the entire Chroma collection and cause
        # Render's 512 MB instance to run out of memory.

        search_count = 10 if is_quick_action else 5

        results = search_documents_with_scores(
            question,
            k=search_count
        )

        for chunk, distance in results:

            if not chunk or len(chunk.strip()) <= 20:
                continue

            # Normal questions:
            # only use genuinely relevant chunks.
            if not is_quick_action:

                if distance < RELEVANCE_THRESHOLD:
                    relevant_chunks.append(chunk)

            # Quick document actions:
            # use the top retrieved chunks even if their distance
            # is slightly above the normal relevance threshold.
            else:

                if distance < 1.0:
                    relevant_chunks.append(chunk)

        used_rag = bool(relevant_chunks)

        print(
            f"RAG: {len(relevant_chunks)} chunks selected "
            f"(quick_action={is_quick_action})"
        )

    except Exception as e:

        print(f"RAG error: {e}")

        relevant_chunks = []
        used_rag = False

    # Build message sent to Groq
    if relevant_chunks:

        context = "\n\n--- DOCUMENT CHUNK ---\n\n".join(
            relevant_chunks
        )

        user_message = f"""
{question}

[Document Context]
The following content was retrieved from the uploaded documents.

{context}

[End Document Context]

Use the document content above to answer the user's request.
"""

    else:

        user_message = question

    conversation_history.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # Keep memory small
    if len(conversation_history) > 20:
        conversation_history = conversation_history[-20:]

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                }
            ] + conversation_history,
            max_tokens=1024,
            temperature=0.7
        )

        answer = response.choices[0].message.content

        conversation_history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        return {
            "answer": answer,
            "used_rag": used_rag,
            "history_length": len(conversation_history)
        }

    except Exception as e:

        if conversation_history:
            conversation_history.pop()

        print(f"AI error: {e}")

        raise HTTPException(
            status_code=500,
            detail=f"AI error: {str(e)}"
        )


@router.get("/chat/history")
async def get_history():

    return {
        "history": conversation_history
    }


@router.delete("/chat/history")
async def clear_history():

    global conversation_history

    conversation_history = []

    return {
        "message": "History cleared"
    }