import logging

import chromadb
from chromadb import QueryResult
from llama_index.core import Document
from langchain_core.documents import Document as LCDocument
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_chroma import Chroma

CALENDAR_COLLECTION = "google_calendar"

CHROMA_DB_PATH = "chromadb"
logger = logging.getLogger(__name__)


def save_google_calendar_documents(documents: list[Document]) -> None:
    logger.info("Saving Google Calendar documents to ChromaDB")
    chroma_client = chromadb.PersistentClient(CHROMA_DB_PATH)
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    collection = chroma_client.create_collection(name="google_calendar", get_or_create=True)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
        length_function=len,
        is_separator_regex=False,
    )
    lc_documents: list[LCDocument] = text_splitter.split_documents([doc.to_langchain_format() for doc in documents])
    Chroma.from_documents(documents=lc_documents, collection_name=CALENDAR_COLLECTION, client=chroma_client, embedding=embedding_function)


def get_google_calendar_relevant_documents(prompt: str) -> QueryResult:
    logger.info("Getting relevant documents from ChromaDB")
    chroma_client = chromadb.PersistentClient(CHROMA_DB_PATH)
    collection = chroma_client.get_collection(name=CALENDAR_COLLECTION)
    results = collection.query(query_texts=prompt)
    return results