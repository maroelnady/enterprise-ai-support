from src.retrieval.chroma_store import search_chroma
from src.retrieval.faiss_store import search_faiss


TEST_CASES = [
    {
        "domain": "vpn",
        "question": "What approval is required for VPN access?",
        "expected_source": "vpn_access_policy.txt",
    },
    {
        "domain": "account",
        "question": "How do I reset my company password?",
        "expected_source": "password_reset_policy.txt",
    },
    {
        "domain": "account",
        "question": "What should I do if my account is locked?",
        "expected_source": "account_lockout_procedure.txt",
    },
    {
        "domain": "email",
        "question": "How do I configure company email?",
        "expected_source": "email_setup_guide.txt",
    },
    {
        "domain": "email",
        "question": "Why is my email not synchronizing?",
        "expected_source": "email_troubleshooting.txt",
    },
    {
        "domain": "sharepoint",
        "question": "How do I request access to a SharePoint site?",
        "expected_source": "sharepoint_access_policy.txt",
    },
    {
        "domain": "sharepoint",
        "question": "What should I do if SharePoint says access denied?",
        "expected_source": "sharepoint_troubleshooting.txt",
    },
    {
        "domain": "security",
        "question": "What should I do if I receive an unexpected MFA request?",
        "expected_source": "cybersecurity_mfa_policy.txt",
    },
]


def evaluate_store(store_name, search_function):
    print("\n" + "=" * 90)
    print(f"{store_name.upper()} MULTI-DOMAIN RETRIEVAL EVALUATION")
    print("=" * 90)

    passed = 0
    total = len(TEST_CASES)

    for case in TEST_CASES:
        question = case["question"]
        expected_source = case["expected_source"]

        results = search_function(question, k=3)

        retrieved_sources = [
            document.metadata.get("filename", "")
            for document, score in results
        ]

        top_source = retrieved_sources[0] if retrieved_sources else ""

        if expected_source in retrieved_sources:
            status = "PASS"
            passed += 1
        else:
            status = "FAIL"

        print("\n" + "-" * 90)
        print(f"Domain          : {case['domain']}")
        print(f"Question        : {question}")
        print(f"Expected source : {expected_source}")
        print(f"Top result      : {top_source}")
        print(f"Retrieved       : {retrieved_sources}")
        print(f"Status          : {status}")

        for i, (document, score) in enumerate(results, start=1):
            print(
                f"  {i}. {document.metadata['filename']} "
                f"| domain={document.metadata['domain']} "
                f"| score={score:.4f}"
            )

    print("\n" + "=" * 90)
    print(f"{store_name.upper()} SUMMARY")
    print("=" * 90)
    print(f"Passed : {passed}/{total}")
    print(f"Failed : {total - passed}/{total}")

    return passed, total


def main():
    chroma_passed, total = evaluate_store(
        "ChromaDB",
        search_chroma
    )

    faiss_passed, _ = evaluate_store(
        "FAISS",
        search_faiss
    )

    print("\n" + "=" * 90)
    print("FINAL COMPARISON")
    print("=" * 90)

    print(f"ChromaDB : {chroma_passed}/{total}")
    print(f"FAISS    : {faiss_passed}/{total}")

    if chroma_passed == total and faiss_passed == total:
        print("\nRESULT: Both vector stores passed all retrieval tests.")
    elif chroma_passed == faiss_passed:
        print("\nRESULT: Both vector stores achieved the same score.")
    else:
        print("\nRESULT: The vector stores produced different retrieval results.")


if __name__ == "__main__":
    main()
