# RAG Dentistry Customer Support Telegram Chatbot : Llama2, Langchain, Pinecone

A Customer Support chatbot built using FastAPI, Llama2, Langchain, and Pinecone. The chatbot utilizes generative AI for providing medical-related assistance and responses. It's designed to offer interactive and intelligent support for users seeking Dental-related information.

## Technology Stack Overview

- **FastAPI(Web Framework)**: FastAPI is a modern and high-performance Python web framework used to build APIs quickly and efficiently.
- **Telegram*(Frontend)**: Telegram serves as a frontend, a user interface, for chatbots, allowing users to interact with automated programs through a familiar messaging interface
- **Llama2(LLM)**: Provides AI-powered responses based on user input.
- **Langchain(LLM framework)**: Facilitates the integration of language models for better response generation.
- **Pinecone(Vector Store)**: Manages and stores vectors to enable semantic search for medical information.
- **Medical resource(Knowledge base)**:[The GALE ENCYCLOPEDIA of MEDICINE](https://www.academia.edu/32752835/The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND_EDITION)
- **Deployment** : Deploy locally, once everything works locally, you can deploy to a server (e.g., Railway, Render, Vercel)

## 🚀 Setup Guide


### Prerequisites

- Python 3.8+
- FastAPI
- python-telegram-bot
- Llama2 model
- Langchain
- Pinecone  

Prerequisites before cloning the repo :
- create telegram bot (discussed below)
- create a vector index in Pinecone, upload your own document


### ✅ 1. Create a Telegram Bot

1. Open **Telegram** and search for `@BotFather`.
2. Start a chat and send the command:

   ```
   /start
   ```
3. Create a new bot by typing:

   ```
   /newbot
   ```
4. Provide:

   * **Bot Name** (e.g., "MySupportBot")
   * **Username** (must end with `bot`, e.g., "my_support_bot")
5. BotFather will send you a **Bot Token** like:

   ```
   123456789:ABCdefGhijkLmnoPQRstuVwxyZ
   ```
6. **Save this token** — you’ll need it for `.env`.

---

### ✅ 2. Clone the Repository

```bash
git clone https://github.com/Sarach-git/dentist_assistant

```

---

### ✅ 3. Create and Update the `.env` File

Create a `.env` file in the project root and add your values; To enable retrieval-augmented generation (RAG), you need to create a vector index in Pinecone and upload your own documents.


```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
PINECONE_API_KEY=your_openai_api_key_here

```

---

### ✅ 4. Install Dependencies
*it is recommended to create virtual env*

```bash
pip install -r requirements.txt
```

---

### ✅ 5. Run the Chatbot Locally

```bash
python app.py
```
---

### ✅ 6. Test the Bot

1. Open **Telegram**
2. Find your bot by its username (e.g., `@my_support_bot`)
3. Send a test message — your chatbot should respond!

---


## Contributing

Feel free to fork the repository, make changes, and submit a pull request if you want to contribute to the project.

## License

This project is licensed under the MIT License.


