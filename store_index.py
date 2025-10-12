from src.helper import load_pdf, text_split, download_embedding_model
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os
import time

# ----------------- Set variables -------------------
"""
# create 2 index : dentistry info & general info for 2 seperate docs

1- dentist_info -> 
index_name="dentist-info"
data_path = "/Users/saracharmchi/openAI_API/Dentistry_Chatbot/policy"
chunk_size = 250
chunk_overlap = 50
------------------------------------
2- general_info -> 
index_name = "general-info"
data_path = "/Users/saracharmchi/openAI_API/Dentistry_Chatbot/data"
chunk_size = 500
chunk_overlap = 20
"""
index_name = "dentist-info"
data_path = "/Users/saracharmchi/openAI_API/Dentistry_Chatbot/policy"
chunk_size = 150
chunk_overlap = 75

# ----------------- Set Environment Variables -------------------
load_dotenv()
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)


# OPTIONAL – Create index only if not exists
try:
    pc.describe_index(index_name)
except Exception:
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

# Wait for the index to be ready
while not pc.describe_index(index_name).status["ready"]:
    time.sleep(1)

index = pc.Index(index_name)

# ✅ Check index stats BEFORE inserting new vectors
stats = index.describe_index_stats()
vector_count = stats.get("total_vector_count", 0)

print(f"Total vectors in index: {vector_count}")

if vector_count == 0:
    # ➤ Only embed if no vectors exist
    print("No vectors found—processing and inserting the document...")

    extracted_doc = load_pdf(data_path)
    text_chunks = text_split(
        extracted_data=extracted_doc, chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    embeddings = download_embedding_model()

    vectorstore_from_docs = PineconeVectorStore.from_documents(
        text_chunks, index_name=index_name, embedding=embeddings
    )
    print("✅ Document embedded and stored in Pinecone.")

else:
    # ➤ Skip insertion if vectors already exist
    print("✅ Index already contains vectors. Skipping embedding.")
    # You can still load it like this:
    embeddings = download_embedding_model()
    docsearch = PineconeVectorStore.from_existing_index(
        index_name=index_name, embedding=embeddings
    )

print(index.describe_index_stats())
