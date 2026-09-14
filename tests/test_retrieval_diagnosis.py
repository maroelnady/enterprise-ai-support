from src.retrieval.chroma_store import search_chroma


QUESTION = "How do I request access to a SharePoint site?"


def main():
    print("\n" + "=" * 90)
    print("RETRIEVAL DIAGNOSIS")
    print("=" * 90)

    print(f"\nQuestion:\n{QUESTION}")

    results = search_chroma(QUESTION, k=5)

    print("\n" + "-" * 90)
    print("TOP 5 RETRIEVED CHUNKS")
    print("-" * 90)

    for i, (document, score) in enumerate(results, start=1):
        print("\n" + "=" * 90)
        print(f"Rank       : {i}")
        print(f"Score      : {score:.4f}")
        print(f"Filename   : {document.metadata['filename']}")
        print(f"Domain     : {document.metadata['domain']}")
        print("-" * 90)
        print(document.page_content)


if __name__ == "__main__":
    main()

