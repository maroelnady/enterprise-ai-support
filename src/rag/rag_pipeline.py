from langchain_groq import ChatGroq
from dotenv import load_dotenv

from src.retrieval.chroma_store import search_chroma

load_dotenv()


def build_context(results):
    """
    Convert retrieved documents into a context string
    that will be given to the LLM.
    """

    context_parts = []

    for i, (document, score) in enumerate(results, start=1):

        source = document.metadata.get("filename", "Unknown")

        context_parts.append(
            f"[Source {i}: {source}]\n"
            f"{document.page_content}"
        )

    return "\n\n".join(context_parts)


def generate_answer(question, k=3):
    """
    Retrieve relevant knowledge from ChromaDB
    and generate an answer using Groq.
    """

    # Step 1: Retrieve relevant chunks
    results = search_chroma(question, k=k)

    # Step 2: Build context
    context = build_context(results)

    # Step 3: Create the LLM
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0
    )

    # Step 4: Create the prompt
    prompt = f"""
You are an Enterprise IT Support Assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the answer cannot be found in the context,
say that the information is not available in the
knowledge base.

Do not invent policies, procedures, or technical details.

Context:
{context}

User Question:
{question}

Provide a clear and concise answer.
"""

    # Step 5: Ask the LLM
    response = llm.invoke(prompt)

    return response.content, results


if __name__ == "__main__":

    questions = [
        "What approval is required for VPN access?",
        "How do I set up the VPN?",
        "What should I do if VPN authentication fails?"
    ]

    for question in questions:

        print("\n" + "=" * 80)
        print(f"QUESTION: {question}")

        answer, results = generate_answer(question)

        print("\nANSWER:")
        print(answer)

        print("\nSOURCES:")

        for document, score in results:
            print(
                f"- {document.metadata['filename']} "
                f"(score={score:.4f})"
            )