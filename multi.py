from langchain.agents.agent_types import AgentType
from langchain.chains import RetrievalQA
from langchain.agents import AgentExecutor, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.tools import BaseTool, StructuredTool, tool

from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
from langchain_pinecone import PineconeVectorStore
import pinecone
from pinecone import Pinecone, ServerlessSpec
from tqdm.autonotebook import tqdm
from langchain.prompts import PromptTemplate

# from langchain.llms import CTransformers
from langchain_community.llms import CTransformers
from langchain.llms import OpenAI

from dotenv import load_dotenv
import os
from src.prompt import prompt_template

from telegram import Update, ForceReply
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
import logging


# ---------------- Logging ----------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# ------------------------- Set Environmental Variables  -------------------
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
token = os.getenv("TELEGRAM_BOT_TOKEN")

# ------------------------- Vector Store -------------------

index_name = "medical-chatbot"
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(index_name)
print(index.describe_index_stats())

index_name = "dentist-info"
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(index_name)
print(index.describe_index_stats())

# ------------------------- LLM -------------------
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)
chain_type_kwargs = {"prompt": PROMPT}

llm = OpenAI(openai_api_key=openai_api_key)


# ------------------- Retriever -----------------------
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


# ------------------- Define Tools -----------------------
@tool
def general_info(query: str) -> str:
    """Use this for general medical knowledge, diseases, symptoms, treatments, medications, and health conditions. DO NOT use for clinic-specific information."""
    return retriever_qa_1.run(query)


@tool
def dentist_info(query: str) -> str:
    """Use this for ANY questions about OUR DENTAL CLINIC: schedules, appointments, doctors, prices, services, policies, contact information, or specific clinic details."""
    return retriever_qa_2.run(query)


tools = [general_info, dentist_info]


# ------------------- Initialize Agent -----------------------
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
agent_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
    handle_parsing_errors=True,
)


# agent_chain.run({'input': 'What is the name of the docotrs on saturdays?'})


# ---------------- Telegram bot Setup ----------------


# Start the bot
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        rf"Hi {user.mention_markdown_v2()}\! I\'m a bot powered by OpenAI\. Ask me anything\."
    )


# Help command
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("Ask me any question, and I'll try to answer using AI!")


# Respond
def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle user messages and generate responses using Langchain."""
    user_message = update.message.text

    try:
        # Generate a response using Langchain and OpenAI
        # response = chain.run(question=user_message)
        # response = qa({"query": user_message})
        response = agent_chain.run({"input": user_message})
        update.message.reply_text(response)
    except Exception as e:
        update.message.reply_text(
            "Sorry, I couldn't process your request at the moment."
        )
        logger.error(f"Error: {e}")


# Error handler
def error_handler(update: Update, context: CallbackContext) -> None:
    """Log Errors caused by Updates."""
    logger.warning(f'Update "{update}" caused error "{context.error}"')


# _______________ bot ___________________


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # On different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # On non-command i.e. message - handle the message
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, handle_message)
    )

    # Log all errors
    dispatcher.add_error_handler(error_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM, or SIGABRT
    updater.idle()


if __name__ == "__main__":
    main()
