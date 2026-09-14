#It will determine the likely domain + intent of the user's question before retrieval.
"""
Simple rule-based query router for the Enterprise IT Support system.

The router identifies:
1. The likely IT domain.
2. The likely user intent.

This is the first Advanced RAG improvement.
Later, this component can be replaced by an LLM-based router.
"""


def route_query(question: str):
    question_lower = question.lower()

    # ---------------------------------------------------------
    # Domain detection
    # ---------------------------------------------------------

    if any(word in question_lower for word in [
        "vpn",
        "remote access",
    ]):
        domain = "vpn"

    elif any(word in question_lower for word in [
        "password",
        "account",
        "locked",
        "lockout",
        "login",
        "sign in",
        "signin",
    ]):
        domain = "account"

    elif any(word in question_lower for word in [
        "email",
        "mailbox",
        "mail",
        "synchronize",
        "synchronizing",
    ]):
        domain = "email"

    elif any(word in question_lower for word in [
        "sharepoint",
        "site",
        "document library",
    ]):
        domain = "sharepoint"

    elif any(word in question_lower for word in [
        "mfa",
        "multi-factor",
        "multi factor",
        "phishing",
        "security",
        "suspicious",
        "compromised",
    ]):
        domain = "security"

    else:
        domain = "unknown"

     # ---------------------------------------------------------
        # Intent detection
        #
        # IMPORTANT:
        # Specific intents must be checked before broad intents.
        # ---------------------------------------------------------
    
        # Security incidents must be checked first because questions
        # such as "unexpected MFA request" contain the word "request".
    if any(word in question_lower for word in [
        "unexpected mfa",
        "unexpected authentication",
        "suspicious",
        "phishing",
        "compromised",
    ]):
        intent = "security_incident"
    
        # Troubleshooting must be checked before access_request
        # because phrases such as "access denied" contain "access".
    elif any(word in question_lower for word in [
        "not working",
        "fails",
        "failed",
        "failure",
        "problem",
        "issue",
        "error",
        "denied",
        "doesn't work",
        "cannot",
        "can't",
        "not synchronizing",
        "not synchronized",
        "not syncing",
        "synchronization",
    ]):
        intent = "troubleshooting"
    
    elif any(word in question_lower for word in [
        "reset",
        "forgot",
        "expired",
        "change password",
    ]):
        intent = "password_reset"
    
    elif any(word in question_lower for word in [
        "locked",
        "lockout",
    ]):
        intent = "account_lockout"
    
    elif any(word in question_lower for word in [
        "setup",
        "set up",
        "configure",
        "configuration",
        "install",
    ]):
        intent = "setup"
    
        # Access request is deliberately checked after troubleshooting.
    elif any(word in question_lower for word in [
        "request",
        "apply",
        "approval",
        "access",
    ]):
        intent = "access_request"
    
    else:
        intent = "general"
    

    return {
        "domain": domain,
        "intent": intent,
    }


if __name__ == "__main__":

    test_questions = [
        "What approval is required for VPN access?",
        "How do I reset my company password?",
        "What should I do if my account is locked?",
        "How do I configure company email?",
        "Why is my email not synchronizing?",
        "How do I request access to a SharePoint site?",
        "What should I do if SharePoint says access denied?",
        "What should I do if I receive an unexpected MFA request?",
    ]

    print("\n" + "=" * 80)
    print("QUERY ROUTER TEST")
    print("=" * 80)

    for question in test_questions:
        result = route_query(question)

        print("\n" + "-" * 80)
        print(f"Question : {question}")
        print(f"Domain   : {result['domain']}")
        print(f"Intent   : {result['intent']}")

