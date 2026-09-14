from dotenv import load_dotenv
from langchain_groq import ChatGroq

from src.agents.tools import (
    knowledge_search_tool,
    ticket_creation_tool
)


# Load environment variables from .env
load_dotenv()


def create_llm():
    """
    Create the Groq language model used by the IT Support Agent.
    """
    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0
    )


def build_context(results):
    """
    Convert retrieved knowledge into a clean context string
    for the language model.
    """
    context_parts = []

    for i, item in enumerate(results, start=1):
        source = item["source"]
        content = item["content"]

        context_parts.append(
            f"[Source {i}: {source}]\n{content}"
        )

    return "\n\n".join(context_parts)


def is_ticket_request(question: str) -> bool:
    """
    Detect whether the user explicitly wants an IT ticket created.
    """

    ticket_keywords = [
        "create a ticket",
        "open a ticket",
        "raise a ticket",
        "submit a ticket",
        "log a ticket",
        "create ticket",
        "open ticket",
        "raise ticket",
        "submit ticket",
        "log ticket",
    ]

    question_lower = question.lower()

    return any(
        keyword in question_lower
        for keyword in ticket_keywords
    )


def ask_it_support(question: str):
    """
    Process an IT support question.

    If the user explicitly requests a ticket,
    use the Ticket Creation Tool.

    Otherwise, use the Knowledge Search Tool
    and generate a grounded answer.
    """

    # ---------------------------------------------------------
    # 1. CHECK FOR TICKET REQUEST
    # ---------------------------------------------------------

    if is_ticket_request(question):

        ticket = ticket_creation_tool(
            issue=question
        )

        return {
            "question": question,
            "domain": "unknown",
            "intent": "ticket_creation",
            "answer": (
                "Your IT support ticket has been created successfully.\n\n"
                f"Ticket ID: {ticket['ticket_id']}\n"
                f"Category: {ticket['category']}\n"
                f"Priority: {ticket['priority']}\n"
                f"Status: {ticket['status']}"
            ),
            "sources": []
        }

    # ---------------------------------------------------------
    # 2. KNOWLEDGE SEARCH
    # ---------------------------------------------------------

    search_result = knowledge_search_tool(
        question,
        k=3
    )

    route = {
        "domain": search_result["domain"],
        "intent": search_result["intent"],
    }

    results = search_result["results"]

    # ---------------------------------------------------------
    # 3. BUILD CONTEXT
    # ---------------------------------------------------------

    context = build_context(results)

    # ---------------------------------------------------------
    # 4. CREATE LLM
    # ---------------------------------------------------------

    llm = create_llm()

    # ---------------------------------------------------------
    # 5. CREATE GROUNDED PROMPT
    # ---------------------------------------------------------

    prompt = f"""
You are an Enterprise IT Support Agent.

User question:
{question}

Detected domain:
{route["domain"]}

Detected intent:
{route["intent"]}

Retrieved enterprise knowledge:

{context}

Instructions:

1. Answer the user's question directly.
2. Use ONLY information explicitly supported by the retrieved knowledge.
3. Do NOT use general knowledge to add company-specific systems,
   applications, contact methods, procedures, approval processes,
   or technical details.
4. Do NOT invent examples.
5. If the knowledge base says something such as
   "approved IT Service Desk process", do not assume a specific
   system such as ServiceNow, email, or phone unless it is explicitly
   mentioned in the retrieved knowledge.
6. If a required detail is not present in the knowledge base, say:
   "The available knowledge base does not specify this detail."
7. Preserve the meaning and requirements of the documented procedure.
8. Use clear numbered steps when the answer describes a procedure.
9. End with a short Sources section using the retrieved filenames.
10. Do not expose semantic scores, intent scores, ranking scores,
    or internal retrieval details.

Provide a concise, professional enterprise IT support answer.
"""

    # ---------------------------------------------------------
    # 6. GENERATE ANSWER
    # ---------------------------------------------------------

    response = llm.invoke(prompt)

    # ---------------------------------------------------------
    # 7. RETURN STRUCTURED RESULT
    # ---------------------------------------------------------

    unique_sources = list(
        dict.fromkeys(
            item["source"]
            for item in results
        )
    )

    return {
        "question": question,
        "domain": route["domain"],
        "intent": route["intent"],
        "answer": response.content,
        "sources": unique_sources
    }


# =============================================================
# TEST THE IT SUPPORT AGENT
# =============================================================

if __name__ == "__main__":

    # ---------------------------------------------------------
    # TEST QUESTION
    # ---------------------------------------------------------

    question = (
        "Create a ticket because I cannot access "
        "the SharePoint Finance site."
    )

    result = ask_it_support(question)

    # ---------------------------------------------------------
    # DISPLAY RESULT
    # ---------------------------------------------------------

    print("\n" + "=" * 90)
    print("IT SUPPORT AGENT")
    print("=" * 90)

    print(f"\nQuestion:\n{result['question']}")

    print(f"\nDomain:\n{result['domain']}")

    print(f"\nIntent:\n{result['intent']}")

    print(f"\nAnswer:\n{result['answer']}")

    print("\nSources:")

    if result["sources"]:
        for source in result["sources"]:
            print(f" - {source}")
    else:
        print(" - None")

