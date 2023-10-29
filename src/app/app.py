from langchain.chains import ConversationalRetrievalChain
from langchain.llms.openai import OpenAI

from src.chatbot_interface import streamlit_chatbot_app
from src.doc_store import DocStore
from src.utils.data import download_and_unzip

REPO_ZIP_URL = "https://github.com/langchain-ai/langchain/archive/refs/heads/master.zip"
TARGET_EXTENSIONS = [".md", ".mdx"]


if __name__ == "__main__":
    download_and_unzip(REPO_ZIP_URL, TARGET_EXTENSIONS, force_new_download=False)

    doc_store = DocStore()
    llm = OpenAI(temperature=0)
    retriever = doc_store.db.as_retriever(search_kwargs={"k": 10})
    chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        return_source_documents=True,
        return_generated_question=True,
    )

    streamlit_chatbot_app(chain)
