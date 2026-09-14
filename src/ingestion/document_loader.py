from pathlib import Path
from langchain_core.documents import Document


DATA_DIR = Path("data/raw")


def load_txt_documents(data_dir: Path = DATA_DIR):
    """
    Load all TXT documents from the knowledge-base directory.

    Returns:
        list[Document]: LangChain Document objects
    """

    documents = []

    for file_path in data_dir.rglob("*.txt"):

        # Read document content
        text = file_path.read_text(encoding="utf-8")

        # Remove document-ending markers that do not contain useful knowledge
        text = text.replace("End of Document", "").strip()

        # Determine domain from folder name
        domain = file_path.parent.name

        # Extract basic metadata
        metadata = {
            "source": str(file_path),
            "filename": file_path.name,
            "domain": domain,
        }

        # Create LangChain Document
        document = Document(
            page_content=text,
            metadata=metadata
        )

        documents.append(document)

    return documents


if __name__ == "__main__":

    documents = load_txt_documents()

    print(f"\nLoaded documents: {len(documents)}\n")

    for i, doc in enumerate(documents, start=1):

        print("=" * 70)
        print(f"Document {i}")
        print(f"Source : {doc.metadata['source']}")
        print(f"Domain : {doc.metadata['domain']}")
        print(f"Chars  : {len(doc.page_content)}")
        print()

        # Show first 200 characters
        print(doc.page_content[:200])