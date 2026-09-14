from dotenv import load_dotenv
from crewai import Agent, LLM

from src.agents.crewai_groq_compat import remove_cache_breakpoints


load_dotenv()


# ============================================================
# CREWAI / GROQ LLM
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
# MANAGER / ORCHESTRATOR AGENT
# ============================================================

def create_manager_agent():

    llm = create_crewai_llm()

    agent = Agent(
        role="Enterprise IT Support Manager",

        goal=(
            "Analyze employee IT support requests and determine "
            "which specialist agent should handle each request."
        ),

        backstory=(
            "You are the manager and orchestrator of an enterprise "
            "IT support system. You understand the responsibilities "
            "of different specialist agents and route requests to "
            "the most appropriate specialist. "
            "You do not invent enterprise policies, procedures, "
            "technical details, or support actions."
        ),

        verbose=True,

        allow_delegation=True,

        llm=llm,
    )

    return agent


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    agent = create_manager_agent()

    print("=" * 70)
    print("CREWAI MANAGER / ORCHESTRATOR AGENT")
    print("=" * 70)

    print("\nAgent created successfully.")
    print(f"Role: {agent.role}")
    print(f"Goal: {agent.goal}")
