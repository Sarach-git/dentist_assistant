from setuptools import find_packages, setup

setup(
    name="dentistryChatbot",
    version="0.0.1",
    author="sara charmchi",
    author_email="charmchisara@yahoo.com",
    install_requires=["openai", "langchain", "streamlit", "python-dotenv", "PyPDF2"],
    packages=find_packages(),
)
