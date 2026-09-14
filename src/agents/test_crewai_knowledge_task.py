from crewai import Crew, Process

from src.agents.crewai_knowledge_agent import create_knowledge_agent
from src.agents.crewai_knowledge_tasks import create_knowledge_task


def run_test():

    knowledge_agent = create_knowledge_agent()

    user_request = (
        "How do I request access to a SharePoint site?"
    )

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

    print("\n" + "=" * 80)
    print("CREWAI KNOWLEDGE SPECIALIST TASK TEST COMPLETE")
    print("=" * 80)

    print("\nFINAL ANSWER:")
    print(result)


if __name__ == "__main__":
    run_test()
