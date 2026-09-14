from crewai import Task


def create_manager_task(manager, user_request: str):
    return Task(
        description=(
            f"Analyze the following employee IT support request:\n\n"
            f"{user_request}\n\n"
            "Choose exactly ONE specialist from the following options:\n\n"
            "knowledge\n"
            "it_support\n\n"
            "Routing rules:\n"
            "- Use knowledge when the request is primarily a question "
            "that requires searching the approved enterprise knowledge base.\n"
            "- Use it_support when the request involves IT troubleshooting, "
            "an IT support issue, or explicit creation/opening/submission/"
            "logging of an IT ticket.\n\n"
            "Return ONLY the selected routing value.\n"
            "Do not provide an explanation.\n"
            "Do not answer the employee's request.\n"
            "Do not invent enterprise policies, procedures, technical "
            "details, or support actions."
        ),
        expected_output=(
            "Exactly one routing value: "
            "'knowledge' or 'it_support'."
        ),
        agent=manager,
    )