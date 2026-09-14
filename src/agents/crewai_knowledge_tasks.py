from crewai import Task


def create_knowledge_task(agent, user_request: str):
    """
    Create a task for the Enterprise Knowledge Specialist.

    The specialist must use the approved enterprise knowledge
    search tool and provide a grounded answer.
    """

    return Task(
        description=(
            f"Answer the following employee IT support question:\n\n"
            f"{user_request}\n\n"

            "Use the Enterprise Knowledge Search tool to retrieve "
            "the relevant approved enterprise documentation.\n\n"

            "Base the answer only on the retrieved enterprise "
            "knowledge. Include the relevant source document names "
            "when available.\n\n"

            "If the required information is not available in the "
            "retrieved knowledge, clearly state that the information "
            "is not available.\n\n"

            "Do not invent company-specific policies, procedures, "
            "approval requirements, technical details, or contact "
            "methods."
        ),

        expected_output=(
            "A concise, professional answer to the employee's question "
            "grounded in the approved enterprise knowledge base, "
            "including relevant source document names."
        ),

        agent=agent,
    )
