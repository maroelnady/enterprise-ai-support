import json
from pathlib import Path
from datetime import datetime

from src.retrieval.routed_retrieval import search_with_routing


# =============================================================
# FILE CONFIGURATION
# =============================================================


TICKETS_FILE = Path("data/tickets.json")


# =============================================================
# KNOWLEDGE SEARCH TOOL
# =============================================================


def knowledge_search_tool(question: str, k: int = 3):
    """
    Search the enterprise knowledge base and return
    relevant documents for an IT support question.
    """

    results, route = search_with_routing(question, k=k)

    output = {
        "domain": route["domain"],
        "intent": route["intent"],
        "results": []
    }

    for (
        document,
        semantic_score,
        intent_score,
        domain_bonus,
        ranking_score
    ) in results:

        output["results"].append({
            "source": document.metadata.get(
                "filename",
                "Unknown"
            ),
            "content": document.page_content,
            "semantic_score": semantic_score,
            "intent_score": intent_score,
            "domain_bonus": domain_bonus,
            "ranking_score": ranking_score,
        })

    return output


# =============================================================
# TICKET CATEGORY DETECTION
# =============================================================

def detect_ticket_category(issue: str) -> str:
    """
    Detect the IT support category from the issue description.
    """

    issue_lower = issue.lower()

    if "sharepoint" in issue_lower:
        return "SharePoint"

    if (
        "vpn" in issue_lower
        or "remote access" in issue_lower
    ):
        return "VPN"

    if (
        "email" in issue_lower
        or "mailbox" in issue_lower
        or "mail" in issue_lower
    ):
        return "Email"

    if (
        "password" in issue_lower
        or "account" in issue_lower
        or "locked" in issue_lower
        or "lockout" in issue_lower
    ):
        return "Account"

    if (
        "mfa" in issue_lower
        or "multi-factor" in issue_lower
        or "phishing" in issue_lower
        or "suspicious" in issue_lower
    ):
        return "Security"

    return "General IT"


# =============================================================
# TICKET PRIORITY DETECTION
# =============================================================

def detect_ticket_priority(issue: str) -> str:
    """
    Detect ticket priority from the issue description.
    """

    issue_lower = issue.lower()

    high_priority_keywords = [
        "security incident",
        "phishing",
        "compromised",
        "account compromised",
        "unexpected mfa",
        "multiple users",
        "company-wide",
        "system down",
    ]

    medium_priority_keywords = [
        "cannot access",
        "can't access",
        "access denied",
        "not working",
        "not synchronizing",
        "not synchronized",
        "not syncing",
        "synchronization",
        "synchronize",
        "synchronizing",
        "error",
        "failed",
        "failure",
        "unable to",
    ]

    if any(
        keyword in issue_lower
        for keyword in high_priority_keywords
    ):
        return "High"

    if any(
        keyword in issue_lower
        for keyword in medium_priority_keywords
    ):
        return "Medium"

    return "Low"


# =============================================================
# TICKET CREATION TOOL
# =============================================================

def ticket_creation_tool(issue: str):
    """
    Create a simulated IT support ticket and save it
    to the local tickets.json file.
    """

    category = detect_ticket_category(issue)
    priority = detect_ticket_priority(issue)

    TICKETS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if TICKETS_FILE.exists():

        with open(
            TICKETS_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            tickets = json.load(file)

    else:
        tickets = []

    ticket_number = len(tickets) + 1

    ticket_id = f"IT-{ticket_number:05d}"

    ticket = {
        "ticket_id": ticket_id,
        "issue": issue,
        "category": category,
        "priority": priority,
        "status": "Open",
        "created_at": datetime.now().isoformat(
            timespec="seconds"
        )
    }

    tickets.append(ticket)

    with open(
        TICKETS_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            tickets,
            file,
            indent=4
        )

    return ticket