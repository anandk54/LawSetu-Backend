from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance

qdrant_client = QdrantClient(
    url="http://localhost:6333",
    api_key=None
)
collection_name = "lawsetu_emd"
if collection_name not in [c.name for c in qdrant_client.get_collections().collections]:
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )