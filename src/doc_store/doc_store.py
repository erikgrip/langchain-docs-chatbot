import os
from glob import glob

from dotenv import load_dotenv
from langchain.document_loaders.base import BaseLoader
from langchain.text_splitter import (MarkdownHeaderTextSplitter,
                                     RecursiveCharacterTextSplitter,
                                     TextSplitter)

from src.utils.log import logger

load_dotenv()  # take environment variables from .env
hf_api_token = os.getenv("HF_API_TOKEN")



# TODO: Implement DocStore
class DocStore:
    def __init__(self, doc_loader_cls: BaseLoader, text_splitter: TextSplitter, doc_file_exts: list[str], **kwargs: dict):
        self.doc_loader_cls = doc_loader_cls
        self.text_splitter = text_splitter(*kwargs)
        self.doc_file_exts = doc_file_exts
        self.args = kwargs

    def load(self, path):
        pass

    def save(self, path):
        pass

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

    def split_docs(self, docs):
        """Split a list of documents into chunks of text."""
        return [self.text_splitter.split_text(doc) for doc in docs]
    

        
