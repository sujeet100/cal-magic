import logging

from openai import OpenAI
from openai.types.chat import ChatCompletion

from cal_magic.db.embeddings import get_google_calendar_relevant_documents

GPT_4o_MINI = "gpt-4o-mini"
logger = logging.getLogger(__name__)


def get_open_api_response(prompt: str) -> ChatCompletion:
    logger.info(f"Wait...")
    embeddings = get_google_calendar_relevant_documents(prompt)
    enriched_prompt = (f'Answer the following question: "{prompt} with context in triple quotes.'
                       f'"""{embeddings}"""')
    client = OpenAI()

    completion = client.chat.completions.create(
        model=GPT_4o_MINI,
        messages=[
            {"role": "system", "content": "You are a personal assistant who managed the google calendar."},
            {"role": "user", "content": enriched_prompt}
        ]
    )

    return completion
