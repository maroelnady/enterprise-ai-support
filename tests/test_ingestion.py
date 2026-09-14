from src.ingestion.document_loader import load_txt_documents


def main():

    documents = load_txt_documents()

    print("\n========== INGESTION TEST ==========")

    print(f"Total documents: {len(documents)}")

    domains = set(
        doc.metadata["domain"]
        for doc in documents
    )

    print(f"Domains: {domains}")

    print("\nDocument list:")

    for doc in documents:
        print(
            f"- {doc.metadata['filename']} "
            f"| domain={doc.metadata['domain']}"
        )


if __name__ == "__main__":
    main()