# pylint: disable=protected-access
import os
import shutil
import tempfile
from unittest.mock import patch

import pytest
from langchain.docstore.document import Document
from langchain.vectorstores.chroma import Chroma

from src.doc_store import DocStore


@pytest.mark.parametrize(
    ("delete_persisted_db"),
    [(True), (False)],
)
class TestGroup:
    """Test group for DocStore."""

    @pytest.fixture(name="doc_store")
    def fixture_doc_store(self, delete_persisted_db):
        """Create a temporary DocStore."""
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = os.path.join(tmpdir, "data")
            persist_dir = os.path.join(tmpdir, "persist_dir")

            # Create a test document
            os.makedirs(data_path)
            with open(os.path.join(data_path, "test.md"), "w", encoding="utf-8") as f:
                f.write("# Test Document\n\nThis is a test document.")

            # Yield the DocStore object with a mocked embedding
            with patch(
                "src.doc_store.OpenAIEmbeddings.embed_documents"
            ) as mock_embedding:
                mock_embedding.return_value = [0.0, 0.0, 0.0]
                ds = DocStore(
                    data_path, delete_persisted_db, db_persist_dir=persist_dir
                )
                yield ds
                shutil.rmtree(tmpdir)

    def test_create_db(self, doc_store):
        """Test creating a new Chroma database."""
        assert doc_store.db is not None

    def test_db_from_docs_dir(self, doc_store):
        """ "Make sure the index has expected size."""
        assert len(doc_store.db.get(include=[])["ids"]) == 1

    def test_add_docs_with_retry(self, doc_store):
        """Test adding documents to Chroma database with retry."""
        docs = [Document(page_content="Test document.", metadata={"id": "test_doc"})]
        doc_store.add_docs(docs)
        assert len(doc_store.db.get(include=[])["ids"]) == 2

    def test_load_docs_from_dir(self, doc_store):
        """Test loading documents from a directory."""
        docs = doc_store._load_docs_from_dir(doc_store.data_path)
        assert len(docs) == 1
        assert docs[0].page_content == "Test Document\n\nThis is a test document."
