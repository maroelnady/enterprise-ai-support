from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.ingestion.document_loader import load_txt_documents


def split_documents(documents):
    """
    Split documents into smaller chunks for RAG.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


if __name__ == "__main__":

    documents = load_txt_documents()

    chunks = split_documents(documents)

    print("\n========== CHUNKING TEST ==========")
    print(f"Original documents: {len(documents)}")
    print(f"Total chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks, start=1):

        print("\n" + "=" * 70)
        print(f"Chunk {i}")

        print(f"Source : {chunk.metadata['filename']}")
        print(f"Domain : {chunk.metadata['domain']}")
        print(f"Characters : {len(chunk.page_content)}")

        print("\nContent:")
        print(chunk.page_content)