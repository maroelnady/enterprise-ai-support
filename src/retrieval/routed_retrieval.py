from src.retrieval.chroma_store import search_chroma
from src.retrieval.query_router import route_query


def get_intent_keywords(intent: str):
    """
    Return keywords associated with each user intent.
    These keywords are used to improve retrieval ranking.
    """

    intent_keywords = {
        "access_request": [
            "access policy",
            "access request",
            "approval",
            "provisioning",
            "request access",
            "manager approval",
        ],

        "troubleshooting": [
            "troubleshooting",
            "problem",
            "issue",
            "error",
            "access denied",
            "not working",
            "fails",
        ],

        "security_incident": [
            "security",
            "mfa",
            "suspicious",
            "phishing",
            "unexpected",
            "report",
        ],

        "password_reset": [
            "password reset",
            "reset password",
            "forgot password",
            "self-service",
        ],

        "account_lockout": [
            "account lockout",
            "locked",
            "lockout",
        ],

        "setup": [
            "setup",
            "configure",
            "configuration",
            "installation",
        ],

        "general": []
    }

    return intent_keywords.get(intent, [])


def calculate_intent_score(document, intent: str):
    """
    Give a bonus when document content matches the detected intent.
    Higher score = stronger intent match.
    """

    keywords = get_intent_keywords(intent)

    text = document.page_content.lower()

    matches = sum(
        1 for keyword in keywords
        if keyword.lower() in text
    )

    return matches


def search_with_routing(question: str, k: int = 3):

    # -------------------------------------------------
    # 1. Detect domain and intent
    # -------------------------------------------------

    route = route_query(question)

    domain = route["domain"]
    intent = route["intent"]

    # -------------------------------------------------
    # 2. Retrieve semantic candidates
    # -------------------------------------------------

    candidates = search_chroma(question, k=5)

    # -------------------------------------------------
    # 3. Re-rank candidates
    # -------------------------------------------------

    ranked_candidates = []

    for document, semantic_score in candidates:

        document_domain = document.metadata.get("domain", "")

        # Intent matching
        intent_score = calculate_intent_score(
            document,
            intent
        )

        # Domain bonus
        domain_bonus = 1 if document_domain == domain else 0

        # -------------------------------------------------
        # Final ranking score
        #
        # Lower semantic distance is better.
        # Therefore we SUBTRACT bonuses.
        # -------------------------------------------------

        ranking_score = (
            semantic_score
            - (intent_score * 0.20)
            - (domain_bonus * 0.10)
        )

        ranked_candidates.append(
            (
                document,
                semantic_score,
                intent_score,
                domain_bonus,
                ranking_score
            )
        )

    # -------------------------------------------------
    # 4. Sort by final ranking score
    # -------------------------------------------------

    ranked_candidates.sort(
        key=lambda item: item[4]
    )

    return ranked_candidates[:k], route


if __name__ == "__main__":

    questions = [
        "How do I request access to a SharePoint site?",
        "What should I do if SharePoint says access denied?",
        "What should I do if I receive an unexpected MFA request?",
    ]

    print("\n" + "=" * 100)
    print("INTENT-AWARE RETRIEVAL TEST")
    print("=" * 100)

    for question in questions:

        results, route = search_with_routing(
            question,
            k=3
        )

        print("\n" + "-" * 100)

        print(f"Question : {question}")
        print(f"Domain   : {route['domain']}")
        print(f"Intent   : {route['intent']}")

        print("\nRetrieved and re-ranked results:")

        for i, (
            document,
            semantic_score,
            intent_score,
            domain_bonus,
            ranking_score
        ) in enumerate(results, start=1):

            print(
                f"{i}. "
                f"{document.metadata['filename']} "
                f"| domain={document.metadata['domain']} "
                f"| semantic={semantic_score:.4f} "
                f"| intent={intent_score} "
                f"| domain_bonus={domain_bonus} "
                f"| final={ranking_score:.4f}"
            )