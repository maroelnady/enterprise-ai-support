from crewai import Crew, Process

from src.agents.crewai_manager_agent import create_manager_agent
from src.agents.crewai_manager_tasks import create_manager_task

from src.agents.crewai_knowledge_agent import create_knowledge_agent
from src.agents.crewai_it_support_agent import create_it_support_agent


def run_test():

    manager = create_manager_agent()
    knowledge_agent = create_knowledge_agent()
    it_support_agent = create_it_support_agent()

    # Give the Manager explicit knowledge about the specialists.
    manager.backstory = (
        "You are the manager and orchestrator of an enterprise IT "
        "support system.\n\n"

        "You have two specialist agents available:\n\n"

        "1. Enterprise Knowledge Specialist:\n"
        "Handles employee questions that require searching the "
        "approved enterprise knowledge base.\n\n"

        "2. Enterprise IT Support Specialist:\n"
        "Handles IT troubleshooting, support requests, and explicit "
        "requests to create IT tickets.\n\n"

        "Your responsibility is to analyze each request and delegate "
        "the work to the appropriate specialist. "
        "Do not solve the employee's request yourself. "
        "Do not invent enterprise policies, procedures, technical "
        "details, or support actions."
    )

    user_request = (
        "How do I request access to a SharePoint site?"
    )

    manager_task = create_manager_task(
        manager=manager,
        user_request=user_request,
    )

    # Explicitly allow the Manager to delegate work.
    manager.allow_delegation = True

    crew = Crew(
        agents=[
            manager,
            knowledge_agent,
            it_support_agent,
        ],

        tasks=[
            manager_task,
        ],

        process=Process.sequential,

        verbose=True,
    )

    result = crew.kickoff()

    print("\n" + "=" * 80)
    print("CREWAI MANAGER DELEGATION TEST COMPLETE")
    print("=" * 80)

    print("\nFINAL ANSWER:")
    print(result)


if __name__ == "__main__":
    run_test()
