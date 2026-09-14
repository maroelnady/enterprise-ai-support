from pathlib import Path

import chromadb
from langchain_chroma import Chroma

from src.ingestion.document_loader import load_txt_documents
from src.ingestion.chunker import split_documents
from src.embeddings.embedding_model import load_langchain_embedding_model


CHROMA_DIR = Path("vectorstores/chroma")
COLLECTION_NAME = "enterprise_it_support"


def build_chroma_store():
    """
    Load documents, split them into chunks,
    generate embeddings, and store them in ChromaDB.
    """

    print("\n========== BUILDING CHROMA STORE ==========")

    # 1. Load documents
    documents = load_txt_documents()

    print(f"Documents loaded: {len(documents)}")

    # 2. Split documents into chunks
    chunks = split_documents(documents)

    print(f"Chunks created: {len(chunks)}")

    # 3. Load embedding model
    embedding_model = load_langchain_embedding_model()

    print("Embedding model loaded.")

    # 4. Create persistent Chroma vector store
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_DIR),
    )

    print(f"ChromaDB collection: {COLLECTION_NAME}")
    print(f"Storage location: {CHROMA_DIR}")

    return vectorstore


def search_chroma(query, k=3):
    """
    Search ChromaDB for the most relevant chunks.
    """
  

    embedding_model = load_langchain_embedding_model()

    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_DIR),
        embedding_function=embedding_model,
    )

    results = vectorstore.similarity_search_with_score(
        query,
        k=k
    )

    return results


if __name__ == "__main__":

    vectorstore = build_chroma_store()

    query = "What approval is required for VPN access?"

    print("\n========== SEARCH TEST ==========")
    print(f"Question: {query}")

    results = search_chroma(query, k=3)

    for i, (document, score) in enumerate(results, start=1):

        print("\n" + "=" * 70)
        print(f"Result {i}")
        print(f"Score: {score:.4f}")
        print(f"Source: {document.metadata['filename']}")
        print(f"Domain: {document.metadata['domain']}")

        print("\nContent:")
        print(document.page_content)