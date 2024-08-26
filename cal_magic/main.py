from cal_magic.goog.calendar import read_calendar_events
from cal_magic.db.embeddings import save_google_calendar_documents
from cal_magic.openapi.openapi import get_open_api_response
from colorama import Fore

def cal_magic():
    events = read_calendar_events()
    save_google_calendar_documents(events)
    prompt = ""
    while prompt != "bye":
        prompt = input(f"{Fore.MAGENTA}>")
        response = get_open_api_response(prompt)
        for choice in response.choices:
            print(f"{Fore.GREEN}{choice.message.content}")



def configure_logging() -> None:
    import logging

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )



if __name__ == '__main__':
    configure_logging()
    cal_magic()