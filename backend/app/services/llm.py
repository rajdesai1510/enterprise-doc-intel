from langchain_groq import ChatGroq
from app.core.config import settings

llm = ChatGroq(
    groq_api_key=settings.groq_api_key,
    model_name="llama-3.1-8b-instant",  # fast + free-tier friendly
    temperature=0.2
)

def generate_answer(prompt: str) -> str:
    response = llm.invoke(prompt)
    return response.content
