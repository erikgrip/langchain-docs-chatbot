# pylint: disable=unspecified-encoding
import logging
import os
import shutil
from glob import glob

from dotenv import load_dotenv
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
from tqdm import tqdm

from src.utils.log import logger


load_dotenv()
logging.getLogger("unstructured").setLevel(logging.WARNING)

CHUNK_SIZE = 1_000
CHUNK_OVERLAP = 100
FILE_EXTS = [".md", "mdx"]
REPO_ID = "sentence-transformers/all-mpnet-base-v2"
DB_PERSIST_DIR = "data/chroma/"
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
RECREATE_DB = False


class DocStore:
    """Document store using Chroma."""

    def __init__(self, data_path, delete_persisted_db=False, **kwargs):
        """Initialize DocStore."""
        self.args = {
            "chunk_size": kwargs.get("chunk_size", CHUNK_SIZE),
            "chunk_overlap": kwargs.get("chunk_overlap", CHUNK_OVERLAP),
            "file_exts": kwargs.get("file_exts", FILE_EXTS),
            "repo_id": kwargs.get("repo_id", REPO_ID),
            "persist_directory": kwargs.get("db_persist_dir", DB_PERSIST_DIR),
            "recreate_db": kwargs.get("recreate_db", RECREATE_DB),
        }

        self.doc_loader = UnstructuredMarkdownLoader
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.args["chunk_size"], chunk_overlap=self.args["chunk_overlap"]
        )
        self.embedding = OpenAIEmbeddings()
        if delete_persisted_db:
            if os.path.exists(self.args["persist_directory"]):
                logger.info("Removing persisted data...")
                shutil.rmtree(self.args["persist_directory"])
            self.create_db()
            self.db_from_docs_dir(data_path)
        else:
            self.create_db()
            if len(self.db.get(include=[])["ids"]) == 0:
                logger.info("No documents found in database. Creating a new one...")
                self.db_from_docs_dir(data_path)

    def create_db(self):
        """Create a new Chroma database."""
        self.db = Chroma(
            persist_directory=self.args["persist_directory"],
            embedding_function=self.embedding,
        )

    def db_from_docs_dir(self, dir_path):
        """Load all documents from a directory and its subdirectories."""
        docs = self._load_docs_from_dir(dir_path)
        split_docs = self.text_splitter.split_documents(docs)

        logger.info("Creating Chroma database...")
        chunk_size = 50
        for i in tqdm(range(0, len(split_docs), chunk_size)):
            chunk_end = min(i + chunk_size, len(split_docs))
            self._add_docs_with_retry(split_docs[i:chunk_end])
        logger.info("Done!")

    def _add_docs_with_retry(self, docs, max_retries=4):
        """Add documents to Chroma database with retry."""
        retries = 0
        try:
            self.db.add_documents(docs)
        except KeyError:
            retries += 1
            if retries > max_retries:
                raise
            logger.error("Failed to add documents to Chroma database. Retrying...")
            self._add_docs_with_retry(docs)

    def _load_docs_from_dir(self, dir_path):
        """Load all documents from a directory and its subdirectories."""
        loaders = [
            self.doc_loader(path)
            for path in glob(dir_path + "/**", recursive=True)
            if path.endswith(tuple(self.args["file_exts"]))
        ]
        logging.info("Loading documents...")
        docs = []
        for loader in tqdm(loaders):
            docs.extend(loader.load())
        return docs
