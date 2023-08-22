from glob import glob
from langchain.document_loaders.base import BaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.utils.log import logger

# TODO: Implement DocStore
class DocStore:
    def __init__(self, doc_loader: BaseLoader, doc_file_exts: list[str]):
        self.doc_loader = doc_loader
        self.doc_file_exts = doc_file_exts

    def load(self, path): 
        pass

    def save(self, path):
        pass

    def load_docs_from_dir(self, dir_path):
        """Load all documents from a directory and its subdirectories."""
        loaders = [
            self.doc_loader(path)
            for path in glob(dir_path + "/**", recursive=True)
            if path.endswith(tuple(self.doc_file_exts))
        ]
        docs = []
        for loader in loaders:
            docs.extend(loader.load())
        return docs

    def _split_doc(self, doc):
        """Split a document into chunks of text using langchains RecursiveCharacterTextSplitter."""
        logger.info(f"Splitting document {doc.id} into chunks of text.")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=100
        )
        # TODO: Finish this function
