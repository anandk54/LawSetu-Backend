import uuid
from langchain_community.embeddings import HuggingFaceEmbeddings
from qdrant_client.models import PointStruct
from app.db.vector_store import qdrant_client

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def embed_document(text: str) -> str:
    vector = embeddings.embed_query(text)
    point_id = str(uuid.uuid4())

    qdrant_client.upsert(
        collection_name="lawsetu_emd",
        points=[
            PointStruct(id=point_id, vector=vector, payload={"text": text})
        ],
    )
    return point_id