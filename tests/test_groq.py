import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


def main():

    print("\n========== GROQ TEST ==========")

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY was not found. "
            "Check your .env file."
        )

    print("API key loaded successfully.")

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
    )

    response = llm.invoke(
        "Explain in one sentence what RAG means."
    )

    print("\n========== RESPONSE ==========")
    print(response.content)


if __name__ == "__main__":
    main()