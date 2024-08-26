import logging

from llama_index.core import Document
from llama_index.readers.google import GoogleCalendarReader
logger = logging.getLogger(__name__)

def read_calendar_events() -> list[Document]:
    logger.info("Getting events from google calendar...")
    reader = GoogleCalendarReader()
    documents = reader.load_data()
    logger.info("Done")
    return documents
