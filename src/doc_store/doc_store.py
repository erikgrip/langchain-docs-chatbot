import os
from glob import glob

from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.embeddings import HuggingFaceEmbeddings, HuggingFaceHubEmbeddings
from langchain.text_splitter import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain.vectorstores import Chroma
from tqdm import tqdm

from src.utils.log import logger

load_dotenv()  # take environment variables from .env


HF_API_TOKEN = os.getenv("HF_API_TOKEN")


# TODO: Implement DocStore
class DocStore:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 100,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.doc_file_exts = [".md", "mdx"]

        self.doc_loader_cls = UnstructuredMarkdownLoader
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        self.embedding = HuggingFaceHubEmbeddings(
            huggingfacehub_api_token=HF_API_TOKEN,
            repo_id="sentence-transformers/all-mpnet-base-v2",
        )

        self.chroma_persist_dir = "data/chroma/"
        self.db = Chroma(
            embedding_function=self.embedding,
            persist_directory=self.chroma_persist_dir,
        )

    def load(self, path):
        pass

    def save(self, path):
        pass

    def db_from_dir(self, dir_path):
        """Load all documents from a directory and its subdirectories."""
        docs = self.load_docs_from_dir(dir_path)
        split_docs = self.text_splitter.split_documents(docs)

        logger.info("Creating Chroma database...")
        # Add texts to Chroma in chunks of 50 documents
        chunk_size = 50
        for i in tqdm(range(0, len(split_docs), chunk_size)):
            self.add_docs_with_retry(split_docs[i : i + chunk_size])
        logger.info("Created Chroma database.")

    def add_docs_with_retry(self, docs, max_retries=4):
        """Add documents to Chroma database with retry."""
        retries = 0
        try:
            self.db.add_documents(docs)
        except KeyError:
            retries += 1
            if retries > max_retries:
                raise
            logger.error("Failed to add documents to Chroma database. Retrying...")
            self.add_docs_with_retry(docs)

    def load_docs_from_dir(self, dir_path):
        """Load all documents from a directory and its subdirectories."""
        loaders = [
            self.doc_loader_cls(path)
            for path in glob(dir_path + "/**", recursive=True)
            if path.endswith(tuple(self.doc_file_exts))
        ]
        docs = []
        for loader in loaders:
            docs.extend(loader.load())
        return docs
