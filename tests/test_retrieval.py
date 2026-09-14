from src.retrieval.chroma_store import search_chroma


def main():

    questions = [
        "What approval is required for VPN access?",
        "How do I set up the VPN?",
        "What should I do if VPN authentication fails?"
    ]

    print("\n========== RETRIEVAL EVALUATION ==========")

    for question in questions:

        print("\n" + "=" * 80)
        print(f"QUESTION: {question}")

        results = search_chroma(question, k=3)

        for i, (document, score) in enumerate(results, start=1):

            print(f"\n--- Result {i} ---")
            print(f"Score : {score:.4f}")
            print(f"Source: {document.metadata['filename']}")
            print(f"Domain: {document.metadata['domain']}")
            print(f"Content:\n{document.page_content}")


if __name__ == "__main__":
    main()