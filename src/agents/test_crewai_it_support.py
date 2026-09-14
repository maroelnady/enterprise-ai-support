from crewai import Crew, Process

from src.agents.crewai_it_support_agent import create_it_support_agent
from src.agents.crewai_it_support_tasks import create_it_support_task


def run_test():

    agent = create_it_support_agent()

    user_request = (
        "The employee cannot access the SharePoint Finance site. "
        "Create an IT support ticket for this issue."
    )

    task = create_it_support_task(
        agent=agent,
        user_request=user_request,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    print("\n" + "=" * 80)
    print("CREWAI IT SUPPORT REUSABLE TASK TEST COMPLETE")
    print("=" * 80)
    print("\nFINAL ANSWER:")
    print(result)


if __name__ == "__main__":
    run_test()
