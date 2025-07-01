import os
from typing import List
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

class VectorStoreService:
    def __init__(self, collection_name: str = "lawsetu-knowledge-base"):
        self.collection_name = collection_name

        # Qdrant connection settings
        qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")  # Optional for local

        # Initialize HuggingFace embeddings
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key
        )

        # Create collection if it doesn't exist
        existing_collections = [c.name for c in self.qdrant_client.get_collections().collections]
        if self.collection_name not in existing_collections:
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
            )

        # Initialize LangChain Qdrant vector store
        self.vectorstore = Qdrant(
            client=self.qdrant_client,
            collection_name=self.collection_name,
            embeddings=self.embeddings
        )

    def add_documents(self, documents: List[str]): 
        # Add a list of text documents to the vector store.
        self.vectorstore.add_texts(documents)

    def similarity_search(self, query: str, k: int = 5) -> List[str]:
        # Retrieve top-k most similar documents to the query.
        results = self.vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in results]

