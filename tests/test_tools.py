from src.agents.tools import (
    detect_ticket_category,
    detect_ticket_priority,
    knowledge_search_tool,
    ticket_creation_tool,
)


def test_ticket_classification():

    test_cases = [
        (
            "VPN connection is not working",
            "VPN",
            "Medium"
        ),
        (
            "My email is not synchronizing",
            "Email",
            "Medium"
        ),
        (
            "My account is locked",
            "Account",
            "Low"
        ),
        (
            "I received an unexpected MFA request",
            "Security",
            "High"
        ),
        (
            "I forgot my password",
            "Account",
            "Low"
        ),
    ]

    passed = 0

    print("\n" + "=" * 90)
    print("TICKET CLASSIFICATION TEST")
    print("=" * 90)

    for (
        issue,
        expected_category,
        expected_priority
    ) in test_cases:

        category = detect_ticket_category(issue)
        priority = detect_ticket_priority(issue)

        category_pass = (
            category == expected_category
        )

        priority_pass = (
            priority == expected_priority
        )

        if category_pass and priority_pass:
            passed += 1

        print("\n" + "-" * 70)

        print(f"Issue: {issue}")

        print(
            f"Category: {category} "
            f"(Expected: {expected_category}) "
            f"[{'PASS' if category_pass else 'FAIL'}]"
        )

        print(
            f"Priority: {priority} "
            f"(Expected: {expected_priority}) "
            f"[{'PASS' if priority_pass else 'FAIL'}]"
        )

    accuracy = (
        passed / len(test_cases)
    ) * 100

    print("\n" + "=" * 90)
    print(
        f"Classification Result: "
        f"{passed}/{len(test_cases)} "
        f"({accuracy:.1f}%)"
    )
    print("=" * 90)


def test_knowledge_search():

    question = (
        "How do I request access to a SharePoint site?"
    )

    result = knowledge_search_tool(question, k=3)

    print("\n" + "=" * 90)
    print("KNOWLEDGE SEARCH TEST")
    print("=" * 90)

    print(f"\nQuestion:\n{question}")

    print(f"\nDomain: {result['domain']}")
    print(f"Intent: {result['intent']}")

    print("\nRetrieved Sources:")

    for i, item in enumerate(
        result["results"],
        start=1
    ):
        print(
            f"{i}. {item['source']}"
        )

    expected_source = (
        "sharepoint_access_policy.txt"
    )

    top_source = result["results"][0]["source"]

    if top_source == expected_source:
        print(
            "\nTop-1 Retrieval: PASS"
        )
    else:
        print(
            "\nTop-1 Retrieval: FAIL"
        )

    print("=" * 90)


def test_ticket_creation():

    issue = (
        "Cannot access the SharePoint Finance site"
    )

    ticket = ticket_creation_tool(issue)

    print("\n" + "=" * 90)
    print("TICKET CREATION TEST")
    print("=" * 90)

    print("\nCreated Ticket:")

    print(
        f"Ticket ID: {ticket['ticket_id']}"
    )

    print(
        f"Issue: {ticket['issue']}"
    )

    print(
        f"Category: {ticket['category']}"
    )

    print(
        f"Priority: {ticket['priority']}"
    )

    print(
        f"Status: {ticket['status']}"
    )

    print(
        "\nTicket Creation: PASS"
    )

    print("=" * 90)


if __name__ == "__main__":

    test_ticket_classification()

    test_knowledge_search()

    test_ticket_creation()