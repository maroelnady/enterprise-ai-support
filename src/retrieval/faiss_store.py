from pathlib import Path

from langchain_community.vectorstores import FAISS

from src.ingestion.document_loader import load_txt_documents
from src.ingestion.chunker import split_documents
from src.embeddings.embedding_model import load_langchain_embedding_model


FAISS_DIR = Path("vectorstores/faiss")


def build_faiss_store():
    """
    Load documents, split them into chunks,
    create embeddings, and store them in FAISS.
    """

    # 1. Load documents
    documents = load_txt_documents()

    # 2. Split documents into chunks
    chunks = split_documents(documents)

    # 3. Load the LangChain embedding model
    embeddings = load_langchain_embedding_model()

    # 4. Create FAISS vector store
    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    # 5. Save FAISS index to disk
    FAISS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    vectorstore.save_local(str(FAISS_DIR))

    print("\n========== BUILDING FAISS STORE ==========")
    print(f"Documents loaded : {len(documents)}")
    print(f"Chunks created   : {len(chunks)}")
    print(f"FAISS location   : {FAISS_DIR}")

    return vectorstore


def search_faiss(question, k=3):
    """
    Search FAISS for the most relevant chunks.
    """

    embeddings = load_langchain_embedding_model()

    vectorstore = FAISS.load_local(
        str(FAISS_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )

    results = vectorstore.similarity_search_with_score(
        question,
        k=k
    )

    return results


if __name__ == "__main__":

    vectorstore = build_faiss_store()

    question = "What approval is required for VPN access?"

    results = search_faiss(
        question,
        k=3
    )

    print("\n========== FAISS SEARCH TEST ==========")
    print(f"Question: {question}")

    for i, (document, score) in enumerate(results, start=1):

        print("\n" + "=" * 70)
        print(f"Result {i}")
        print(f"Score  : {score:.4f}")
        print(f"Source : {document.metadata['filename']}")
        print(f"Domain : {document.metadata['domain']}")

        print("\nContent:")
        print(document.page_content)