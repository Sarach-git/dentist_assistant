import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request
import httpx

from telegram import Update
from telegram.ext import CallbackContext

# LangChain + Pinecone imports
from src.helper import download_embedding_model
from langchain.vectorstores import Pinecone
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from src.prompt import *

# ---------------- Logging ----------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ---------------- Load environment ----------------
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
pinecone_api_key = os.getenv("PINECONE_API_KEY")

# ---------------- Pinecone + LangChain setup ----------------
index_name = "medical-chatbot"
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(index_name)
print(index.describe_index_stats())

embeddings = download_embedding_model()
docsearch = PineconeVectorStore.from_existing_index(index_name, embeddings)

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)
chain_type_kwargs = {"prompt": PROMPT}

llm = CTransformers(
    model="model/llama-2-7b-chat.ggmlv3.q4_0.bin",
    model_type="llama",
    config={"max_new_tokens": 512, "temperature": 0.8},
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever(search_kwargs={"k": 2}),
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs,
)

# ---------------- FastAPI app ----------------
app = FastAPI()


@app.get("/")
def index():
    return {"message": "Bot is running on Vercel 🚀"}


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, None)  # Parse Telegram update

    if update.message and update.message.text:
        chat_id = update.message.chat.id
        user_message = update.message.text

        try:
            response = qa({"query": user_message})
            reply_text = response["result"]
        except Exception as e:
            logger.error(f"Error: {e}")
            reply_text = "Sorry, I couldn't process your request right now."

        async with httpx.AsyncClient() as client:
            await client.post(
                f"{BASE_URL}/sendMessage", json={"chat_id": chat_id, "text": reply_text}
            )

    return {"ok": True}
