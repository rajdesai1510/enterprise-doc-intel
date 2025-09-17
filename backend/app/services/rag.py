from langchain_core.prompts import PromptTemplate
from app.services.retriever import retrieve_chunks
from app.services.llm import generate_answer

prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful AI assistant answering questions from enterprise documents.

Answer the question using ONLY the provided context.
Your answer will be shown along with source citations.

Context:
{context}

Question:
{question}

Rules:
- Use ONLY the context
- Do NOT use outside knowledge
- If the answer is not in the context, say "I don't know"
- Be concise, factual, and neutral
"""
)

def run_rag(query: str, namespace: str):
    contexts, sources = retrieve_chunks(query, namespace)

    if not contexts:
        return {
            "answer": "No relevant information found in your documents.",
            "sources": []
        }

    context_block = "\n\n".join(contexts)

    prompt = prompt_template.format(
        context=context_block,
        question=query
    )

    answer = generate_answer(prompt)

    return {
        "answer": answer,
        "sources": sources
    }
