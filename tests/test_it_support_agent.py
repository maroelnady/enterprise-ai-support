from src.agents.it_support_agent import ask_it_support


def run_test(question: str, expected_domain: str, expected_intent: str):
    print("\n" + "=" * 90)
    print("IT SUPPORT AGENT TEST")
    print("=" * 90)

    print(f"\nQuestion:")
    print(question)

    result = ask_it_support(question)

    print(f"\nDetected Domain:")
    print(result["domain"])

    print(f"\nDetected Intent:")
    print(result["intent"])

    print(f"\nExpected Domain:")
    print(expected_domain)

    print(f"\nExpected Intent:")
    print(expected_intent)

    domain_pass = result["domain"] == expected_domain
    intent_pass = result["intent"] == expected_intent

    print(
        f"\nDomain Check: "
        f"[{'PASS' if domain_pass else 'FAIL'}]"
    )

    print(
        f"Intent Check: "
        f"[{'PASS' if intent_pass else 'FAIL'}]"
    )

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")

    if result["sources"]:
        for source in result["sources"]:
            print(f" - {source}")
    else:
        print(" - None")

    return domain_pass and intent_pass


def main():

    test_cases = [
        (
            "How do I request access to a SharePoint site?",
            "sharepoint",
            "access_request"
        ),
        (
            "My VPN connection is not working.",
            "vpn",
            "troubleshooting"
        ),
        (
            "I received an unexpected MFA request.",
            "security",
            "security_incident"
        ),
    ]

    passed = 0

    for (
        question,
        expected_domain,
        expected_intent
    ) in test_cases:

        result = run_test(
            question,
            expected_domain,
            expected_intent
        )

        if result:
            passed += 1

    print("\n" + "=" * 90)
    print("AGENT EVALUATION SUMMARY")
    print("=" * 90)

    print(
        f"\nPassed: {passed}/{len(test_cases)}"
    )

    accuracy = (
        passed / len(test_cases)
    ) * 100

    print(
        f"Result: {accuracy:.1f}%"
    )

    print("=" * 90)

def test_ticket_request():

    question = (
        "Create a ticket because I cannot access "
        "the SharePoint Finance site."
    )

    print("\n" + "=" * 90)
    print("IT SUPPORT AGENT — TICKET REQUEST TEST")
    print("=" * 90)

    print(f"\nQuestion:")
    print(question)

    result = ask_it_support(question)

    print("\nDetected Domain:")
    print(result["domain"])

    print("\nDetected Intent:")
    print(result["intent"])

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")

    if result["sources"]:
        for source in result["sources"]:
            print(f" - {source}")
    else:
        print(" - None")

    expected_intent = "ticket_creation"

    if result["intent"] == expected_intent:
        print("\nIntent Check: [PASS]")
    else:
        print("\nIntent Check: [FAIL]")


if __name__ == "__main__":
    main()
    test_ticket_request()