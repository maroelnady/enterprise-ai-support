import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


def load_embedding_model():
    """
    Load the local Sentence Transformers embedding model.
    """

    model = SentenceTransformer(MODEL_NAME)

    return model


def create_embeddings(texts):
    """
    Convert a list of text strings into numerical vectors.
    """

    model = load_embedding_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    return embeddings

from langchain_huggingface import HuggingFaceEmbeddings


def load_langchain_embedding_model():
    """
    Load the embedding model using LangChain's
    Embeddings interface.
    """

    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME
    )

    return embeddings

if __name__ == "__main__":

    print("\n========== EMBEDDING TEST ==========")

    model = load_embedding_model()

    print(f"Model: {MODEL_NAME}")
    print(f"Embedding dimension: {model.get_embedding_dimension()}")

    texts = [
        "VPN access requires manager approval.",
        "Employees need approval before receiving VPN access.",
        "The company cafeteria serves lunch."
    ]

    embeddings = create_embeddings(texts)

    print(f"Number of texts: {len(texts)}")
    print(f"Embedding shape: {embeddings.shape}")

    # Calculate cosine similarity
    similarity_ab = np.dot(embeddings[0], embeddings[1])
    similarity_ac = np.dot(embeddings[0], embeddings[2])

    print("\n========== SEMANTIC SIMILARITY ==========")

    print(f"\nSentence A:")
    print(texts[0])

    print(f"\nSentence B:")
    print(texts[1])

    print(f"\nSentence C:")
    print(texts[2])

    print("\nSimilarity A ↔ B:")
    print(f"{similarity_ab:.4f}")

    print("\nSimilarity A ↔ C:")
    print(f"{similarity_ac:.4f}")