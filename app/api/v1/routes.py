from fastapi import APIRouter
from app.services.llm import get_legal_answer
from app.services.embeddings import embed_document
from app.services.embeddings import embed_query
from pydantic import BaseModel
from app.db.vector_store import qdrant_client
from typing import List
from fastapi import File, UploadFile
import json

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
async def query_legal_ai(request: QueryRequest):
    # get the embedding of the query
    # consine similarity in the db
    # top k documnet return
    # pass the query with document to the llm req
    # pass with cleaning the query and adding the proper prompt
    # return the answer

    embeded_query = embed_query(request.question)
    k = 5
    search_result = qdrant_client.search(
        collection_name="lawsetu_emd",
        query_vector=embeded_query,
        limit=k,
    )

    # Extract relevant documents from search results
    relevant_docs = []
    for result in search_result:
        if result.payload:
            doc = {}
            if "section_title" in result.payload:
                doc["section_title"] = result.payload["section_title"]
            if "section_text" in result.payload:
                doc["section_text"] = result.payload["section_text"]
            if "citation" in result.payload:
                doc["citation"] = result.payload["citation"]
            if doc:
                relevant_docs.append(doc)
    
    # Create context from retrieved documents (for LLM)
    context = "\n\n".join([
        f"Title: {doc.get('section_title', '')}\nText: {doc.get('section_text', '')}\nCitation: {doc.get('citation', '')}"
        for doc in relevant_docs
    ])

    # Get answer using LLM with context
    response = get_legal_answer(request.question, context)
    return {"answer": response}


class SectionData(BaseModel):
    document_id: str
    section_number: str
    section_title: str
    section_text: str
    citation: str
    document_title: str
    jurisdiction: str
    date: str

class MultipleSectionRequest(BaseModel):
    documents: List[SectionData]

@router.post("/embed/sections")
async def embed_multiple_sections(request: MultipleSectionRequest):
    vector_ids = []
    for section in request.documents:
        section_data = section.dict()
        vector_id = embed_document(section_data)
        vector_ids.append(str(vector_id))
    return {"vector_ids": vector_ids}

@router.post("/embed/sections/file")
async def embed_multiple_sections_file(file: UploadFile = File(...)):
    contents = await file.read()
    data = json.loads(contents)
    # data is now a list of dicts
    vector_ids = []
    for section_dict in data:
        section = SectionData(**section_dict)  # Validate and parse
        section_data = section.dict()
        vector_id = embed_document(section_data)
        vector_ids.append(str(vector_id))
    return {"vector_ids": vector_ids}