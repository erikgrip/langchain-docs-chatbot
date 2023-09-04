import os
import ssl

import nltk

from langchain.document_loaders import UnstructuredMarkdownLoader
from langchain.embeddings import HuggingFaceHubEmbeddings
from langchain.text_splitter import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

from src.data_downloader.run import DOCS_PATH_IN_REPO, OUTPUT_PATH, download_repo
from src.doc_store.doc_store import DocStore

# HACK: https://github.com/gunthercox/ChatterBot/issues/930#issuecomment-322111087
# TODO: Check if needed in container
try:
    _create_unverified_https_context = (
        ssl._create_unverified_context  # pylint: disable=protected-access
    )
except AttributeError:
    pass
else:
    ssl._create_default_https_context = (  # pylint: disable=protected-access
        _create_unverified_https_context
    )

nltk.download("punkt")


download_repo()
args = {"hf_repo_id": "sentence-transformers/all-mpnet-base-v2"}
doc_store = DocStore()

doc_store.db_from_dir(OUTPUT_PATH + DOCS_PATH_IN_REPO)
