# how to use template.py to make your project folder?
# run python template.py

# how to localise for my project?
# you can change the structre of the project as you wish


import os

PROJECT_STRUCTURE = {
    "app.py": "# Main entry for the chatbot app\n\nif __name__ == '__main__':\n    print('Running app...')\n",
    "retriever.py": "# Handles retrieval of clinic and general knowledge\n",
    "intent.py": "# Intent recognition logic\n",
    "llm.py": "# Interface with the language model\n",
    "config.py": "# Configuration handling\n",
    "requirements.txt": "flask\nlangchain\npinecone-client\nopenai\npython-dotenv\n",
    ".env": "# Add your API keys and configuration here\nOPENAI_API_KEY=\nPINECONE_API_KEY=\n",
    "data": {
        "clinic.json": '{\n  "name": "My Clinic",\n  "address": "123 Main St",\n  "pricing": {},\n  "hours": {},\n  "contacts": {},\n  "services": []\n}\n',
        "faq.md": "# Clinic FAQs\n\n- What are your hours?\n- Do you accept insurance?\n",
        "policies.md": "# Clinic Policies\n\nCancellation Policy:\nPayment Policy:\nInsurance Policy:\n",
    },
    "general_knowledge": {
        "tooth_basics.md": "# Tooth Basics\n\n- Types of teeth\n- Functions\n",
        "hygiene_tips.md": "# Hygiene Tips\n\n- Brush twice a day\n- Floss daily\n",
    },
}


def create_files(base_path: str, structure: dict):
    """
    Recursively create directories and files based on the structure dictionary.
    """
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):  # It's a folder
            os.makedirs(path, exist_ok=True)
            create_files(path, content)
        else:  # It's a file
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)


if __name__ == "__main__":
    project_name = "dentist_chatbot"
    os.makedirs(project_name, exist_ok=True)
    create_files(project_name, PROJECT_STRUCTURE)
    print(f"✅ Project '{project_name}' created successfully!")
