"""
CrewAI Knowledge Agent using Groq
=================================

This file creates our first CrewAI agent and explicitly
configures it to use the Groq LLM.

Why?

CrewAI defaults to OpenAI if no LLM is specified.

Our project already uses Groq successfully:

    Groq
      |
      v
    openai/gpt-oss-120b
      |
      v
    Enterprise IT Support

Therefore, we explicitly configure CrewAI to use the
same provider/model.

Architecture:

    User Question
          |
          v
    CrewAI Knowledge Agent
          |
          +--------------------+
          |                    |
          v                    v
      Groq LLM          Knowledge Search Tool
          |                    |
          |                    v
          |              Existing RAG
          |                    |
          |               ChromaDB
          |                    |
          +---------+----------+
                    |
                    v
              Final Answer
"""


# ============================================================
# 1. IMPORTS
# ============================================================

# Loads variables from the .env file.
#
# Our .env already contains:
#
#     GROQ_API_KEY=...
#
# We NEVER put the actual API key inside this Python file.
from dotenv import load_dotenv

from crewai import Agent, LLM
from crewai.tools import tool

from src.agents.tools import knowledge_search_tool
from src.agents.crewai_groq_compat import remove_cache_breakpoints

# ============================================================
# 2. LOAD ENVIRONMENT VARIABLES
# ============================================================

# Read the .env file.
#
# This makes GROQ_API_KEY available to the application.
load_dotenv()


# ============================================================
# 3. CREATE THE CREWAI LLM
# ============================================================

def create_crewai_llm():
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
# 4. CREATE CREWAI KNOWLEDGE SEARCH TOOL
# ============================================================

@tool("Enterprise Knowledge Search")
def enterprise_knowledge_search(question: str) -> str:
    """
    Search the enterprise IT knowledge base.

    This function connects CrewAI to our existing RAG system.
    """

    # Call the existing intent-aware RAG retrieval.
    result = knowledge_search_tool(
        question,
        k=3
    )


    # Create a list for the formatted result.
    output = []


    # Add detected domain.
    output.append(
        f"Detected domain: {result['domain']}"
    )


    # Add detected intent.
    output.append(
        f"Detected intent: {result['intent']}"
    )


    output.append("")


    # Add heading.
    output.append(
        "Retrieved enterprise knowledge:"
    )


    # --------------------------------------------------------
    # Add retrieved documents
    # --------------------------------------------------------

    for i, item in enumerate(
        result["results"],
        start=1
    ):

        # Add source filename.
        output.append(
            f"\nSource {i}: {item['source']}"
        )

        # Add document content.
        output.append(
            item["content"]
        )


    # Convert the list into one string.
    return "\n".join(output)


# ============================================================
# 5. CREATE THE KNOWLEDGE AGENT
# ============================================================

def create_knowledge_agent():
    """
    Create the CrewAI Enterprise Knowledge Agent.
    """

    # --------------------------------------------------------
    # Create the Groq LLM
    # --------------------------------------------------------

    llm = create_crewai_llm()


    # --------------------------------------------------------
    # Create the CrewAI Agent
    # --------------------------------------------------------

    agent = Agent(

        # ====================================================
        # ROLE
        # ====================================================
        role="Enterprise Knowledge Specialist",


        # ====================================================
        # GOAL
        # ====================================================
        goal=(
            "Answer enterprise IT questions using only "
            "the approved enterprise knowledge base."
        ),


        # ====================================================
        # BACKSTORY
        # ====================================================
        backstory=(
            "You are a specialized enterprise knowledge agent. "
            "You retrieve relevant company IT policies, "
            "procedures, troubleshooting guides, and security "
            "documentation. You must ground your answers in "
            "retrieved enterprise knowledge and must never "
            "invent company-specific procedures."
        ),


        # ====================================================
        # TOOLS
        # ====================================================
        #
        # This agent receives ONLY the knowledge search tool.
        #
        # It does NOT receive the ticket creation tool.
        #
        # This is intentional and demonstrates controlled
        # tool access.
        tools=[
            enterprise_knowledge_search
        ],


        # ====================================================
        # LLM
        # ====================================================
        #
        # THIS IS THE IMPORTANT FIX.
        #
        # We explicitly tell CrewAI to use Groq.
        llm=llm,


        # ====================================================
        # VERBOSE
        # ====================================================
        verbose=True,


        # ====================================================
        # DELEGATION
        # ====================================================
        #
        # The Knowledge Agent is a specialist.
        #
        # It does not delegate work to other agents.
        allow_delegation=False
    )


    return agent


# ============================================================
# 6. OPTIONAL DIRECT TEST
# ============================================================

if __name__ == "__main__":

    # Create the agent.
    knowledge_agent = create_knowledge_agent()


    # Display configuration information.
    print("=" * 70)
    print("CREWAI KNOWLEDGE AGENT")
    print("=" * 70)

    print("\nAgent created successfully.")

    print(
        f"\nRole: {knowledge_agent.role}"
    )

    print(
        f"\nGoal: {knowledge_agent.goal}"
    )

    print("\nLLM:")
    print(" - Provider: Groq")
    print(" - Model: openai/gpt-oss-120b")

    print("\nAvailable tool:")
    print(" - Enterprise Knowledge Search")

    print("\nStatus: READY")
