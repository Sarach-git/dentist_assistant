# note : delete your index first !!!
from src.helper import load_pdf, text_split, download_embedding_model


from langchain.vectorstores import Pinecone
from langchain_pinecone import PineconeVectorStore

import pinecone
from pinecone import Pinecone, ServerlessSpec


from dotenv import load_dotenv
import os
import time

load_dotenv()
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)

index_name = "medical-chatbot"

"""
#if you dont have the index
pc.create_index(
    name=index_name,
    dimension=1024,  # Replace with your model dimensions
    metric="cosine",  # Replace with your model metric
    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
)


"""


# Wait for the index to be ready
while not pc.describe_index(index_name).status["ready"]:
    time.sleep(1)

index = pc.Index(index_name)

extracted_doc = load_pdf("data/")
text_chunks = text_split(extracted_doc)
embeddings = download_embedding_model()


PineconeVectorStore(index_name=index_name, embedding=embeddings)


"""
# if you havent created the vector db:
vectorstore_from_docs = PineconeVectorStore.from_documents(
    text_chunks, index_name=index_name, embedding=embeddings
)
"""


docsearch = PineconeVectorStore.from_existing_index(index_name, embeddings)
print(index.describe_index_stats())
