# Dentistry chatbot

## base model : version 0

**Structure of the project**
1. *Backend component*

medical chatbot based on costum data without rag :
the structure : pdf -> extract data from pdf -> create chunks based on the extracted data -> why chunks? the models like openai or llama2 or other models have some limitations on each execution (input token size)
after creating chunks -> build embedding (convert text chunks to vector embeddings) -> create semantic index
----
### Vector Database

1. Knowledge Base – stores data as embeddings (vectors).

2. Semantic Index – organizes vectors by similarity for fast retrieval.
* Similar concepts (king, queen / man, woman) appear close in vector space.
* Different concepts (monkey) appear in separate regions.
* Clustering can be applied on top to group related vectors.
---

combine all vectors -> build semantic index -> store these vectors in my knowledge base -> what to use as knowledge base ? e.g. Pinecone database (pinecone vs chromadb : pinecone on the cloud database , chromadb is local database)




2. *Frontend component*
user send query -> convert query to query embedding -> sent query embedding to my knowledge base -> knowledge base give you "ranked result ", it means that it will give you the closest vectors to the vector of your query -> extract the exact answer i want with the help of 'LLM' model -> so llm will give the final response ! then i will send it to the user


-----

**technology tools**
programming language : python
generative ai framework : langchain (or llamaIndex)
frontend (UI) for webapp : Flask
LLM : Meta llama2
vector database : Pinecone


-----
**Initial Setup**

create github repository for the project
clone it
create env -> using conda
```bash
conda create -n mchatbot
or
conda create -p env python=3.8 -y
```
and activate the env
then open the vscode, adjust python version in the vscode (3.8)

create requirenments.txt file
```bash
pip install -r requirenments.txt
```
then download the model from hugging face from the following link
```bash
https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/tree/main
```

then create a jupyter notebook for test our functions
