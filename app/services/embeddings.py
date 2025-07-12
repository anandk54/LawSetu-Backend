import uuid
from typing import List
from langchain_community.embeddings import HuggingFaceEmbeddings
from qdrant_client.models import PointStruct
from app.db.vector_store import qdrant_client

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def embed_document(section_data: dict) -> str:
    embedding_vector = embeddings.embed_query(section_data["section_text"])
    
     # Create Qdrant point with metadata payload
    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=embedding_vector,
        payload={
            "document_id": str(section_data["document_id"]),
            "section_number": section_data["section_number"],
            "section_title": section_data["section_title"],
            "section_text": section_data["section_text"],
            "citation": section_data["citation"],
            "document_title": section_data["document_title"],
            "jurisdiction": section_data["jurisdiction"],
            "date": section_data["date"]
        }
    )

    qdrant_client.upsert(
        collection_name="lawsetu_emd",
        points=[point]
    )
    return str(point.id)


def embed_query(text: str) -> List[float]:
    vector = embeddings.embed_query(text)
    return vector