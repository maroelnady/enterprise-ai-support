from src.retrieval.chroma_store import search_chroma
from src.retrieval.routed_retrieval import search_with_routing


TEST_CASES = [
    {
        "question": "How do I request VPN access?",
        "expected": "vpn_access_policy.txt",
    },
    {
        "question": "How do I reset my password?",
        "expected": "password_reset_policy.txt",
    },
    {
        "question": "What should I do if my account is locked?",
        "expected": "account_lockout_procedure.txt",
    },
    {
        "question": "How do I configure my company email?",
        "expected": "email_setup_guide.txt",
    },
    {
        "question": "What should I do if my email is not synchronizing?",
        "expected": "email_troubleshooting.txt",
    },
    {
        "question": "How do I request access to a SharePoint site?",
        "expected": "sharepoint_access_policy.txt",
    },
    {
        "question": "What should I do if SharePoint says access denied?",
        "expected": "sharepoint_troubleshooting.txt",
    },
    {
        "question": "What should I do if I receive an unexpected MFA request?",
        "expected": "cybersecurity_mfa_policy.txt",
    },
]


def evaluate_basic_retrieval():
    top1 = 0
    top3 = 0

    print("\n" + "=" * 100)
    print("BASIC SEMANTIC RETRIEVAL")
    print("=" * 100)

    for case in TEST_CASES:

        results = search_chroma(case["question"], k=3)

        filenames = [
            document.metadata["filename"]
            for document, score in results
        ]

        top1_match = filenames[0] == case["expected"]
        top3_match = case["expected"] in filenames

        if top1_match:
            top1 += 1

        if top3_match:
            top3 += 1

        print(
            f"\nQuestion : {case['question']}"
        )
        print(
            f"Expected : {case['expected']}"
        )
        print(
            f"Retrieved: {filenames}"
        )
        print(
            f"Top-1   : {'PASS' if top1_match else 'FAIL'}"
        )
        print(
            f"Top-3   : {'PASS' if top3_match else 'FAIL'}"
        )

    return top1, top3


def evaluate_intent_retrieval():
    top1 = 0
    top3 = 0

    print("\n" + "=" * 100)
    print("INTENT-AWARE RETRIEVAL")
    print("=" * 100)

    for case in TEST_CASES:

        results, route = search_with_routing(
            case["question"],
            k=3
        )

        filenames = [
            document.metadata["filename"]
            for (
                document,
                semantic_score,
                intent_score,
                domain_bonus,
                ranking_score
            ) in results
        ]

        top1_match = filenames[0] == case["expected"]
        top3_match = case["expected"] in filenames

        if top1_match:
            top1 += 1

        if top3_match:
            top3 += 1

        print(
            f"\nQuestion : {case['question']}"
        )
        print(
            f"Expected : {case['expected']}"
        )
        print(
            f"Domain   : {route['domain']}"
        )
        print(
            f"Intent   : {route['intent']}"
        )
        print(
            f"Retrieved: {filenames}"
        )
        print(
            f"Top-1   : {'PASS' if top1_match else 'FAIL'}"
        )
        print(
            f"Top-3   : {'PASS' if top3_match else 'FAIL'}"
        )

    return top1, top3


def main():

    basic_top1, basic_top3 = evaluate_basic_retrieval()

    intent_top1, intent_top3 = evaluate_intent_retrieval()

    total = len(TEST_CASES)

    print("\n" + "=" * 100)
    print("ADVANCED RAG EVALUATION SUMMARY")
    print("=" * 100)

    print("\nMetric                  Basic Retrieval       Intent-Aware")
    print("-" * 70)

    print(
        f"Top-1                  "
        f"{basic_top1}/{total} "
        f"({basic_top1 / total * 100:.1f}%)"
        f"              "
        f"{intent_top1}/{total} "
        f"({intent_top1 / total * 100:.1f}%)"
    )

    print(
        f"Top-3                  "
        f"{basic_top3}/{total} "
        f"({basic_top3 / total * 100:.1f}%)"
        f"              "
        f"{intent_top3}/{total} "
        f"({intent_top3 / total * 100:.1f}%)"
    )

    improvement = intent_top1 - basic_top1

    print(
        f"\nTop-1 improvement: "
        f"{improvement:+d} question(s)"
    )


if __name__ == "__main__":
    main()