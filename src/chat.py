import ssl

import nltk

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


# download_repo()

doc_store = DocStore()
#doc_store.db_from_docs_dir(OUTPUT_PATH + DOCS_PATH_IN_REPO)

docs = doc_store.db.similarity_search("What is a vector store?")
