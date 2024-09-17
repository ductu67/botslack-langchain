import os

__import__('pysqlite3')
import sys

sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import uuid
from typing import Optional

import chromadb
from chromadb.utils import embedding_functions
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import (
    CSVLoader,
    EverNoteLoader,
    PDFMinerLoader,
    TextLoader,
    UnstructuredEPubLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredODTLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)
from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma

load_dotenv()
CHROMA_PERSISTENCE_DIR = os.environ.get("CHROMA_PERSISTENCE_DIR", "../openai")
CHROMA_COLLECTION = os.environ.get("CHROMA_COLLECTION", "openaiembeddings")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

LOADER_MAPPING = {
    ".csv": (CSVLoader, {"encoding": "utf8"}),
    # ".docx": (Docx2txtLoader, {}),
    ".doc": (UnstructuredWordDocumentLoader, {}),
    ".docx": (UnstructuredWordDocumentLoader, {}),
    ".enex": (EverNoteLoader, {}),
    ".epub": (UnstructuredEPubLoader, {}),
    ".html": (UnstructuredHTMLLoader, {}),
    ".md": (UnstructuredMarkdownLoader, {}),
    ".odt": (UnstructuredODTLoader, {}),
    ".pdf": (PDFMinerLoader, {}),
    ".ppt": (UnstructuredPowerPointLoader, {}),
    ".pptx": (UnstructuredPowerPointLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
    # Add more mappings for other file extensions and loaders as needed
}


class ChromaDB:
    def __init__(self,
                 persistence_dir: Optional[str] = CHROMA_PERSISTENCE_DIR,
                 client: Optional[chromadb.Client] = None,
                 collection_name: str = CHROMA_COLLECTION, ):
        self.persistence_dir = persistence_dir
        self.collection_name = collection_name
        if client:
            self._client = client
        else:
            self._client = chromadb.PersistentClient(path=self.persistence_dir)
        self.openai_ef = embedding_functions.OpenAIEmbeddingFunction(OPENAI_API_KEY)
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.openai_ef,
        )

    def load_document(self, file_path: str):
        ext = "." + file_path.rsplit(".", 1)[-1]
        if ext in LOADER_MAPPING:
            loader_class, loader_args = LOADER_MAPPING[ext]
            loader = loader_class(file_path, **loader_args)
            return loader.load()

        raise ValueError(f"Unsupported file extension '{ext}'")

    def add(self, document, chunk_size: int = 1000, chunk_overlap: int = 0):
        documents = self.load_document(document)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        texts = text_splitter.split_documents(documents)
        ids = [str(uuid.uuid5(uuid.NAMESPACE_DNS, doc.page_content)) for doc in texts]
        unique_ids = list(set(ids))
        seen_ids = set()
        unique_docs = [doc for doc, id in zip(texts, ids) if id not in seen_ids and (seen_ids.add(id) or True)]
        Chroma.from_documents(
            unique_docs,
            embedding=OpenAIEmbeddings(),
            ids=unique_ids,
            client=self._client,
            collection_name=self.collection_name
        )


def list_files_in_directory(folder_path):
    entries = os.listdir(folder_path)
    files = [entry for entry in entries if os.path.isfile(os.path.join(folder_path, entry))]

    return files


folder_path = 'data'
print(list_files_in_directory(folder_path))
for file in list_files_in_directory(folder_path):
    ChromaDB().add(f'data/{file}')
