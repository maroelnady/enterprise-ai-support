import chromadb

client = chromadb.PersistentClient(
    path="vectorstores/chroma"
)

collection = client.get_collection(
    name="enterprise_it_support"
)

print("\n========== CHROMA DATABASE TEST ==========")

print(f"Collection name : {collection.name}")
print(f"Stored chunks   : {collection.count()}")