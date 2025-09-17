from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user
from app.services.rag import run_rag

router = APIRouter(prefix="/query", tags=["Query"])

@router.post("/")
def query_documents(
    question: str,
    namespace: str,
    user=Depends(get_current_user)
):
    result = run_rag(
        query=question,
        namespace=namespace
    )

    return {
        "question": question,
        "answer": result["answer"],
        "sources": result["sources"]
    }
