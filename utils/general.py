import os
import random
from datetime import datetime
from typing import Tuple


def get_variables_from_env() -> Tuple:
    """Get the variables from the environment, explicitly converting
    N_PROCCESS to int.

    Returns:
        Tuple: A tuple containing the variables.
    """
    return int(os.getenv("N_PROCCESS", 1)), os.getenv("URL_TO_CRAWL", None)


def end_process_analytics(
    url_to_crawl: str,
    start_date_time: datetime,
    end_date_time: datetime,
    max_workers: int,
    total_crawled_links: int,
) -> None:
    """Provide some analytical information at the end of crawling proccess.

    Args:
        url_to_crawl (string): The crawled url.
        start_date_time (datetime): The start date and time of the crawling proccess.
        end_date_time (datetime): The end date and time of the crawling proccess.
        max_workers (int): The maximum number of workers.
        console (Console): The console object.

    Returns:
        None
    """
    total_time_elapsed = (end_date_time - start_date_time).total_seconds()

    termwidth, fillchar = 78, '='
    print('/n/n')
    print(' WHAT WE DID HERE? '.center(termwidth, fillchar))
    print("🌐 Intial crawled URL: {}".format(url_to_crawl))
    print("🔗 Crawled a total of {} links.".format(total_crawled_links))
    print("⏱️  The whole proccess took {}s.".format(total_time_elapsed))
    print("⚙️  {} workers were considered to handle this great kob.".format(max_workers))
    print(''.center(termwidth, fillchar))


def get_random_header(original_url: str) -> dict:
    """Based on a small list of know user-agents, return a random header
    to be used in python requests lib, always persisting a referer url reveiced
    as parameter.

    Args:
        original_url (str): The original url used to generate the header.
    """

    user_agent_list = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    ]

    user_agent = random.choice(user_agent_list)

    return {
        "User-Agent": user_agent,
        "Referer": "https://www.google.com/",
    }
