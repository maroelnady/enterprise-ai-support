from crewai import Crew, Process

from src.agents.crewai_manager_agent import create_manager_agent
from src.agents.crewai_manager_tasks import create_manager_task

from src.agents.crewai_knowledge_agent import create_knowledge_agent
from src.agents.crewai_knowledge_tasks import create_knowledge_task

from src.agents.crewai_it_support_agent import create_it_support_agent
from src.agents.crewai_it_support_tasks import create_it_support_task


def run_manager(user_request: str):
    """
    Run the Manager independently and obtain its routing decision.
    """

    manager = create_manager_agent()

    manager_task = create_manager_task(
        manager=manager,
        user_request=user_request,
    )

    crew = Crew(
        agents=[manager],
        tasks=[manager_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    return str(result)


def run_knowledge_specialist(user_request: str):
    """
    Run the Knowledge Specialist only when selected by the Manager.
    """

    knowledge_agent = create_knowledge_agent()

    knowledge_task = create_knowledge_task(
        agent=knowledge_agent,
        user_request=user_request,
    )

    crew = Crew(
        agents=[knowledge_agent],
        tasks=[knowledge_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    return str(result)


def run_it_support_specialist(user_request: str):
    """
    Run the IT Support Specialist only when selected by the Manager.
    """

    it_support_agent = create_it_support_agent()

    it_support_task = create_it_support_task(
        agent=it_support_agent,
        user_request=user_request,
    )

    crew = Crew(
        agents=[it_support_agent],
        tasks=[it_support_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    return str(result)
def route_to_specialist(manager_result: str, user_request: str):
    """
    Route the user request to the specialist selected by the Manager.
    """

    route = manager_result.strip().lower()

    if route == "knowledge":

        print("\nSelected Specialist: Enterprise Knowledge Specialist")

        return run_knowledge_specialist(
            user_request=user_request
        )

    elif route == "it_support":

        print("\nSelected Specialist: Enterprise IT Support Specialist")

        return run_it_support_specialist(
            user_request=user_request
        )

    else:

        raise RuntimeError(
            f"Invalid manager routing decision: {manager_result!r}"
        )

def run_orchestrator(user_request: str):

    print("\n" + "=" * 80)
    print("STEP 1 — MANAGER ROUTING")
    print("=" * 80)

    manager_result = run_manager(user_request)

    print("\nMANAGER RESULT:")
    print(manager_result)

    print("\n" + "=" * 80)
    print("STEP 2 — SPECIALIST EXECUTION")
    print("=" * 80)

    specialist_result = route_to_specialist(
        manager_result=manager_result,
        user_request=user_request,
    )

    print("\n" + "=" * 80)
    print("FINAL SPECIALIST RESULT")
    print("=" * 80)

    print(specialist_result)

    return specialist_result

if __name__ == "__main__":

    user_request = (
        "My SharePoint site is giving me an access denied error. "
        "I cannot open the site even though I was previously able to access it."
    )
