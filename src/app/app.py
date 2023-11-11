import argparse

from langchain.chains import ConversationalRetrievalChain
from langchain.llms.openai import OpenAI

from src.chatbot_interface import streamlit_chatbot_app
from src.doc_store import DocStore
from src.utils.data import download_and_unzip
from src.utils.log import logger

REPO_ZIP_URL = "https://github.com/langchain-ai/langchain/archive/refs/heads/master.zip"
TARGET_EXTENSIONS = [".md", ".mdx"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force_data_download",
        action="store_true",
        help="Force download the data even if it already exists",
    )
    parser.add_argument(
        "--delete_persisted_db",
        action="store_true",
        help="Delete the persisted database and create a new one.",
    )
    parser.add_argument(
        "--num_retrieved_docs",
        type=int,
        default=10,
        help="Number of documents to retrieve from the document store.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Temperature for the OpenAI language model.",
    )
    args = parser.parse_args()
    if args.force_data_download and not args.delete_persisted_db:
        logger.warning("Downloading data without recreating any peristed database.")

    data_path = download_and_unzip(
        REPO_ZIP_URL, TARGET_EXTENSIONS, args.force_data_download
    )
    doc_store = DocStore(data_path, args.delete_persisted_db)
    llm = OpenAI(temperature=args.temperature)
    retriever = doc_store.db.as_retriever(search_kwargs={"k": args.num_retrieved_docs})
    chain = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=retriever,
        return_source_documents=True,
        return_generated_question=True,
    )

    streamlit_chatbot_app(chain)
