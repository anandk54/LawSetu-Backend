import glob
from services.vector_store import VectorStoreService

def chunk_text(text, chunk_size=5):
    # Split text into chunks of N sentences.
    import re
    sentences = re.split(r'(?<=[.!?]) +', text)
    return [' '.join(sentences[i:i+chunk_size]) for i in range(0, len(sentences), chunk_size)]

def process_and_store(folder_pattern):
    vector_service = VectorStoreService()
    files = glob.glob(folder_pattern, recursive=True)
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        chunks = chunk_text(text)
        vector_service.add_documents(chunks)
        print(f"Stored {len(chunks)} chunks from {file_path}")

if __name__ == "__main__":
    process_and_store("dataset/summary/*.txt")
    process_and_store("dataset/judgement/*.txt")