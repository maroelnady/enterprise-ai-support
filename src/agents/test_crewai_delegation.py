from crewai import Crew, Process

from src.agents.crewai_manager_agent import create_manager_agent
from src.agents.crewai_manager_tasks import create_manager_task

from src.agents.crewai_knowledge_agent import create_knowledge_agent
from src.agents.crewai_knowledge_tasks import create_knowledge_task

from src.agents.crewai_it_support_agent import create_it_support_agent
from src.agents.crewai_it_support_tasks import create_it_support_task


def run_test():

    manager = create_manager_agent()
    knowledge_agent = create_knowledge_agent()
    it_support_agent = create_it_support_agent()

    user_request = (
        "How do I request access to a SharePoint site?"
    )

    manager_task = create_manager_task(
        manager=manager,
        user_request=user_request,
    )

    knowledge_task = create_knowledge_task(
        agent=knowledge_agent,
        user_request=user_request,
    )

    it_support_task = create_it_support_task(
        agent=it_support_agent,
        user_request=user_request,
    )

    crew = Crew(
        agents=[
            manager,
            knowledge_agent,
            it_support_agent,
        ],
        tasks=[
            manager_task,
            knowledge_task,
            it_support_task,
        ],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    print("\n" + "=" * 80)
    print("CREWAI MULTI-AGENT DELEGATION TEST COMPLETE")
    print("=" * 80)

    print("\nFINAL RESULT:")
    print(result)


if __name__ == "__main__":
    run_test()
    