import argparse

from src.chatbot_interface import streamlit_chatbot_app
from src.utils.log import logger

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

    streamlit_chatbot_app(
        args.force_data_download,
        args.delete_persisted_db,
        args.num_retrieved_docs,
        args.temperature,
    )
