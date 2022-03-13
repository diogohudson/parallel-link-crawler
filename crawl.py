#!/usr/bin/env python3

import sys
from datetime import datetime

from crawler import init_crawler
from utils import check_procedures, end_process_analytics


def main(max_workers: int, url_to_crawl: str) -> None:
    """
    Based on a supplied amount of workers, and the url to start the crawler,
    create some statistics about the crawling process and start it.
    """
    start_date_time = datetime.now()

    if not check_procedures(url_to_crawl=url_to_crawl, max_workers=max_workers):
        exit(-1)

    total_crawled_links = init_crawler(url_to_crawl, max_workers=max_workers)
    end_date_time = datetime.now()

    end_process_analytics(
        url_to_crawl=url_to_crawl,
        start_date_time=start_date_time,
        end_date_time=end_date_time,
        max_workers=max_workers,
        total_crawled_links=total_crawled_links,
    )

    exit()


if __name__ == "__main__":
    import getopt
    import sys

    argumentList = sys.argv[1:]
    options = "n:"
    long_options = ["workers"]

    arguments, values = getopt.getopt(argumentList, options, long_options)

    for currentArgument, currentValue in arguments:
        if currentArgument in ("-n", "--workers"):
            max_workers = currentValue

    if not max_workers:
        print("Please provide the number of workers")
        exit(-1)

    try:
        url_to_crawl = sys.argv[3]
    except IndexError:
        print("Please provide the url to crawl")
        exit(-1)

    main(max_workers=int(max_workers), url_to_crawl=str(url_to_crawl))
