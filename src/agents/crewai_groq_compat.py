from typing import Any


CACHE_BREAKPOINT_KEY = "cache_breakpoint"


def remove_cache_breakpoints(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Remove CrewAI's internal cache_breakpoint metadata before messages
    are sent to providers that do not support this field.

    The original message dictionaries are not modified.
    """
    cleaned_messages = []

    for message in messages:
        cleaned_message = {
            key: value
            for key, value in message.items()
            if key != CACHE_BREAKPOINT_KEY
        }
        cleaned_messages.append(cleaned_message)

    return cleaned_messages