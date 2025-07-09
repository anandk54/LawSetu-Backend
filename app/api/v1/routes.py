from fastapi import APIRouter
from app.services.llm import get_legal_answer
from app.services.embeddings import embed_document
from pydantic import BaseModel

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
async def query_legal_ai(request: QueryRequest):
    response = get_legal_answer(request.question)
    return {"answer": response}


class DocumentRequest(BaseModel):
    text: str

@router.post("/embed")
async def embed_document_route(request: DocumentRequest):
    vector_id = embed_document(request.text)
    return {"vector_id": vector_id}
