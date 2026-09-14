from src.retrieval.chroma_store import search_chroma
from src.retrieval.faiss_store import search_faiss


QUESTIONS = [
    "What approval is required for VPN access?",
    "How do I set up the VPN?",
    "What should I do if VPN authentication fails?",
]


def print_results(store_name, results):

    print(f"\n--- {store_name} ---")

    for i, (document, score) in enumerate(results, start=1):

        print(
            f"{i}. "
            f"{document.metadata['filename']} "
            f"| score={score:.4f}"
        )


def main():

    print("\n" + "=" * 80)
    print("CHROMA vs FAISS RETRIEVAL EVALUATION")
    print("=" * 80)

    for question in QUESTIONS:

        print("\n" + "-" * 80)
        print(f"QUESTION: {question}")

        chroma_results = search_chroma(
            question,
            k=3
        )

        faiss_results = search_faiss(
            question,
            k=3
        )

        print_results(
            "ChromaDB",
            chroma_results
        )

        print_results(
            "FAISS",
            faiss_results
        )


if __name__ == "__main__":
    main()