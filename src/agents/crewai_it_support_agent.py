from dotenv import load_dotenv
from crewai import Agent, LLM
from crewai.tools import tool

from src.agents.tools import (
    knowledge_search_tool,
    ticket_creation_tool,
)
from src.agents.crewai_groq_compat import remove_cache_breakpoints


load_dotenv()


# ============================================================
# CREWAI / GROQ LLM
# ============================================================

def create_crewai_llm():
    """
    Create the CrewAI LLM using Groq.

    CrewAI adds internal cache_breakpoint metadata to messages.
    Groq does not support this field, so we remove it before
    messages are sent to the provider.
    """

    llm = LLM(
        model="groq/openai/gpt-oss-120b",
        temperature=0,
    )

    original_formatter = llm._format_messages_for_provider

    def groq_safe_formatter(messages):
        formatted = original_formatter(messages)
        return remove_cache_breakpoints(formatted)

    llm._format_messages_for_provider = groq_safe_formatter

    return llm


# ============================================================
# CREWAI TOOLS
# ============================================================

@tool("Enterprise Knowledge Search")
def enterprise_knowledge_search(question: str) -> str:
    """
    Search the approved enterprise IT knowledge base.

    Use this tool when the user needs information about:
    VPN, accounts, passwords, email, SharePoint, security,
    troubleshooting, setup, access requests, or IT procedures.
    """

    result = knowledge_search_tool(
        question=question,
        k=3,
    )

    return str(result)


@tool("IT Ticket Creation")
def create_it_ticket(issue: str) -> str:
    """
    Create an IT support ticket for the user's issue.

    Use this tool only when the user explicitly asks to:
    create, open, raise, submit, or log an IT ticket.
    """

    ticket = ticket_creation_tool(
        issue=issue
    )

    return (
        f"Ticket created successfully.\n"
        f"Ticket ID: {ticket['ticket_id']}\n"
        f"Category: {ticket['category']}\n"
        f"Priority: {ticket['priority']}\n"
        f"Status: {ticket['status']}"
    )


# ============================================================
# CREWAI IT SUPPORT AGENT
# ============================================================

def create_it_support_agent():

    llm = create_crewai_llm()

    agent = Agent(
        role="Enterprise IT Support Specialist",

        goal=(
            "Provide accurate enterprise IT support using the approved "
            "knowledge base and create support tickets when explicitly "
            "requested by the user."
        ),

        backstory=(
            "You are an enterprise IT support specialist. "
            "You help employees with IT procedures and support requests. "
            "For knowledge questions, you must use the Enterprise Knowledge "
            "Search tool and base your answer only on retrieved enterprise "
            "documentation. "
            "For explicit ticket requests, use the IT Ticket Creation tool. "
            "Never invent company-specific procedures, systems, contact "
            "methods, approval processes, or technical details."
        ),

        tools=[
            enterprise_knowledge_search,
            create_it_ticket,
        ],

        verbose=True,

        allow_delegation=False,

        llm=llm,
    )

    return agent


if __name__ == "__main__":

    agent = create_it_support_agent()

    print("=" * 70)
    print("CREWAI IT SUPPORT AGENT")
    print("=" * 70)

    print("\nAgent created successfully.")
    print(f"Role: {agent.role}")
    print(f"Tools: {len(agent.tools)}")
