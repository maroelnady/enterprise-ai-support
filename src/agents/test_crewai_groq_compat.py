from crewai import LLM

llm = LLM(
    model="groq/openai/gpt-oss-120b",
    temperature=0,
)

messages = [
    {
        "role": "system",
        "content": "You are an IT support assistant.",
        "cache_breakpoint": True,
    },
    {
        "role": "user",
        "content": "How do I request SharePoint access?",
        "cache_breakpoint": True,
    },
]

formatted = llm._format_messages_for_provider(messages)

print("FORMATTED MESSAGES:")
print(formatted)

print("\nCACHE BREAKPOINT PRESENT:")
for message in formatted:
    print("cache_breakpoint" in message)