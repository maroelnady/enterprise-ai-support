"""
First CrewAI Knowledge Crew
===========================

This is our first REAL CrewAI execution.

We already created:

    1. Knowledge Agent
    2. Knowledge Task

Now we combine them into:

    3. Crew

Architecture:

    User Question
          |
          v
    Knowledge Agent
          |
          v
    Knowledge Task
          |
          v
    Enterprise Knowledge Search Tool
          |
          v
    Existing RAG
          |
          +--> Query Router
          |
          +--> ChromaDB
          |
          v
    Enterprise Knowledge
          |
          v
    Final Answer
"""


# ============================================================
# 1. IMPORT CREWAI CLASSES
# ============================================================

# Crew is the object responsible for organizing and executing
# our agents and tasks.
from crewai import Crew


# Process controls how CrewAI executes the tasks.
#
# Sequential means:
#
#     Task 1
#       ↓
#     Task 2
#       ↓
#     Task 3
#
# For our first example, we only have one task.
from crewai import Process


# ============================================================
# 2. IMPORT OUR KNOWLEDGE AGENT
# ============================================================

from src.agents.crewai_knowledge_agent import (
    create_knowledge_agent
)


# ============================================================
# 3. IMPORT OUR KNOWLEDGE TASK
# ============================================================

# IMPORTANT:
#
# We are importing the Task that we already created.
#
# This prevents us from duplicating the Task definition.
from src.agents.test_crewai_knowledge_task import (
    knowledge_task
)


# ============================================================
# 4. CREATE THE KNOWLEDGE AGENT
# ============================================================

knowledge_agent = create_knowledge_agent()


# ============================================================
# 5. CREATE THE CREW
# ============================================================

knowledge_crew = Crew(

    # --------------------------------------------------------
    # AGENTS
    # --------------------------------------------------------
    #
    # A Crew can contain multiple agents.
    #
    # Currently we have only one:
    #
    #     Knowledge Agent
    #
    # Later we will have:
    #
    #     Manager Agent
    #     Knowledge Agent
    #     IT Support Agent
    #     Security Agent
    #     Review Agent
    #
    agents=[
        knowledge_agent
    ],


    # --------------------------------------------------------
    # TASKS
    # --------------------------------------------------------
    #
    # These are the assignments that the Crew needs to execute.
    tasks=[
        knowledge_task
    ],


    # --------------------------------------------------------
    # PROCESS
    # --------------------------------------------------------
    #
    # Sequential means the Crew executes tasks in order.
    #
    # We only have one Task now, so this is straightforward.
    #
    # Later, when we have multiple agents and tasks, the
    # process becomes much more interesting.
    process=Process.sequential,


    # --------------------------------------------------------
    # VERBOSE
    # --------------------------------------------------------
    #
    # True allows us to see the execution process.
    #
    # This is useful while learning and debugging.
    verbose=True
)


# ============================================================
# 6. EXECUTE THE CREW
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("FIRST CREWAI KNOWLEDGE CREW")
    print("=" * 70)

    print("\nStarting CrewAI execution...")
    print("\nThe Knowledge Agent will now execute the Task.")
    print("-" * 70)


    # --------------------------------------------------------
    # KICK OFF THE CREW
    # --------------------------------------------------------
    #
    # This is the point where the Crew actually starts working.
    #
    # Until now:
    #
    #     Agent = definition
    #     Task  = definition
    #
    # kickoff() causes actual execution.
    result = knowledge_crew.kickoff()


    # ========================================================
    # 7. DISPLAY THE FINAL RESULT
    # ========================================================

    print("\n")
    print("=" * 70)
    print("CREWAI FINAL RESULT")
    print("=" * 70)

    print("\n")
    print(result)

    print("\n")
    print("=" * 70)
    print("CREWAI EXECUTION COMPLETE")
    print("=" * 70)
