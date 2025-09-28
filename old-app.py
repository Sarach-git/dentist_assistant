from telegram import Update, ForceReply
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

from src.helper import download_embedding_model
from langchain.vectorstores import Pinecone
from langchain_pinecone import PineconeVectorStore
import pinecone
from pinecone import Pinecone, ServerlessSpec
from langchain.prompts import PromptTemplate

# from langchain.llms import CTransformers
from langchain_community.llms import CTransformers

from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os
from src.prompt import *
import logging

# initialize telegram botv log ________________________
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


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


# as experiment file ________________________
load_dotenv()
pinecone_api_key = os.getenv("PINECONE_API_KEY")


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

# define telegram bot ________________________


# Handle messages
def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle user messages and generate responses using Langchain."""
    user_message = update.message.text

    try:
        # Generate a response using Langchain and OpenAI
        # response = chain.run(question=user_message)
        response = qa({"query": user_message})
        update.message.reply_text(response["result"])
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
    # Your Telegram bot token from BotFather
    token = os.getenv("TELEGRAM_BOT_TOKEN")

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
