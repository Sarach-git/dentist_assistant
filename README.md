# Medical Chatbot; Generative AI : Llama2, Langchain, Pinecone

A medical chatbot built using Flask, Llama2, Langchain, and Pinecone. The chatbot utilizes generative AI for providing medical-related assistance and responses. It's designed to offer interactive and intelligent support for users seeking healthcare-related information.

## Features

- **Flask Web App**: A lightweight web server to serve the chatbot interface.
- **Generative AI (Llama2)**: Provides AI-powered responses based on user input.
- **Langchain**: Facilitates the integration of language models for better response generation.
- **Pinecone**: Manages and stores vectors to enable semantic search for medical information.
- **Medical resource**:[The GALE ENCYCLOPEDIA of MEDICINE](https://www.academia.edu/32752835/The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND_EDITION)

## Demo
![Screenshot of demop of medical chatbot.](https://github.com/Sarach-git/mchatbot/demo.png)

## Installation

### Prerequisites

- Python 3.8+
- Flask
- Llama2 model
- Langchain
- Pinecone

### Installation Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/Sarach-git/medical-chatbot.git
   cd medical-chatbot
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up Pinecone by creating an account and getting an API key. Configure it in the `.env` file.

4. Start the Flask app:

   ```bash
   python app.py
   ```

5. Navigate to `http://localhost:8080` in your browser to interact with the chatbot.

## Usage

Simply enter your medical-related query into the chatbot interface. The AI will generate a relevant response based on the context and information available in the knowledge base.

## Contributing

Feel free to fork the repository, make changes, and submit a pull request if you want to contribute to the project.

## License

This project is licensed under the MIT License.


