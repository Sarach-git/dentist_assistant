import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from telegram import Update, Bot

from langchain.agents.agent_types import AgentType
from langchain.chains import RetrievalQA
from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from src.prompt import prompt_template
from pinecone import Pinecone

# ---------------- Logging ----------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------- Environment ----------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)

# ---------------- Vector & LLM Setup ----------------
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)
llm = OpenAI(openai_api_key=OPENAI_API_KEY)
chain_type_kwargs = {"prompt": PROMPT}

pc = Pinecone(api_key=PINECONE_API_KEY)


def retriever_qa_creation(index_name):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    db = PineconeVectorStore.from_existing_index(index_name, embeddings)
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k": 2}),
        chain_type_kwargs=chain_type_kwargs,
    )
    return qa


retriever_qa_1 = retriever_qa_creation("medical-chatbot")
retriever_qa_2 = retriever_qa_creation("dentist-info")


@tool
def general_info(query: str) -> str:
    """General medical questions"""
    return retriever_qa_1.run(query)


@tool
def dentist_info(query: str) -> str:
    """Clinic-specific questions"""
    return retriever_qa_2.run(query)


memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent_chain = initialize_agent(
    [general_info, dentist_info],
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
    handle_parsing_errors=True,
)

# ---------------- FastAPI App ----------------
app = FastAPI()


@app.get("/")
async def home():
    return {"message": "Telegram bot webhook is active!"}


@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        update = Update.de_json(data, bot)
        message = update.message.text if update.message else None
        chat_id = update.message.chat_id if update.message else None

        if message and chat_id:
            response = agent_chain.run({"input": message})
            bot.send_message(chat_id=chat_id, text=response)
    except Exception as e:
        logger.error(f"Error processing update: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

    return JSONResponse(status_code=200, content={"ok": True})
