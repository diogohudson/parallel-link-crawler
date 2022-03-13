import multiprocessing
import threading
from concurrent.futures import ThreadPoolExecutor as Pool
from itertools import repeat
from multiprocessing.managers import ListProxy
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from utils import get_random_header, is_valid_link


def init_crawler(link: str, max_workers: int = None) -> None:
    """Initialize the crawler, by instancing the managers to share the list of
    crawled urls.

    Args:
        link (str): The url to start the crawler.
        max_workers (int): The maximum number of workers.
        lock (threading.Lock): A lock to control access on shared memory.
    """

    manager = multiprocessing.Manager()
    lock = multiprocessing.Lock()
    internal_urls = manager.list()

    crawl(
        link,
        internal_urls,
        initial_url=link,
        max_workers=max_workers,
        lock=lock
    )

    return len(internal_urls)


def crawl(
    link: str, internal_urls: ListProxy, initial_url: str, max_workers: int, lock: multiprocessing.Lock
) -> None:
    """
    Crawls a specific url, extracts all links inside that page and store them
    in a shared memory list, controled as a `set` to avoid duplicates.

    This function, is kind wildy, since it is a recursive function that
    create processes, and child processes. A really simple control based on the
    actual number of workers, is used to prevent creating more processes than
    specified on max_workers what would incur on a army of zomby proccess.

    params:
        link (str): The url to get links from
        internal_urls (ListProxy): A shared memory listing to store the urls.
        initial_url (string): The initial url used to crawl.
        lock (threading.Lock): A lock to control access on shared memory.
    """
    print(link)
    if links := get_all_links_by_url(internal_urls, link=link, initial_url=initial_url, lock=lock):
        active_workers = threading.active_count() - 1
        current_max_workers = max_workers - active_workers
        if current_max_workers > 0:
            with Pool(max_workers=current_max_workers) as pool:
                pool.map(
                    crawl,
                    links,
                    repeat(internal_urls),
                    repeat(initial_url),
                    repeat(max_workers),
                    repeat(lock)
                )

def get_all_links_by_url(internal_urls, link: str, initial_url: str, lock: multiprocessing.Lock) -> set:
    """Get all the links from a website.

    Args:
        internal_urls (ListProxy): A shared memory listing to store the urls.
        initial_url (string): The initial url used to crawl.
        lock (threading.Lock): A lock to control access on shared memory.

    Returns:
        list (set): A set of all the links found on the url.
    """
    try:

        response = requests.get(
            link,
            allow_redirects=True,
            headers=get_random_header(original_url=initial_url),
        )
        if response.ok:
            soup = BeautifulSoup(
                response.content,
                "html.parser",
                from_encoding="iso-8859-1",
            )
            return get_valid_urls_from_a_tags(soup=soup, internal_urls=internal_urls, initial_url=initial_url, lock=lock)

        else:
            return []

    except requests.exceptions.ConnectionError:
        # ignore connection errors, what would prevent execution.
        pass


def get_valid_urls_from_a_tags(
    soup: BeautifulSoup, internal_urls: ListProxy, initial_url: str, lock: multiprocessing.Lock
) -> set:
    """Find all the urls from a BeautifulSoup object.

    Args:
        soup (BeautifulSoup): A valid BeautifulSoup object.
        url (string): The url of the page the soup object belongs to.
        internal_urls (ListProxy): A shared memory listing to store the urls.
        initial_url (string): The initial url used to crawl.
        lock (threading.Lock): A lock to control access on shared memory.

    Returns:
        set: A set with all the urls found in the BeautifulSoup object.
    """
    new_urls_set = set()

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")

        if href == "" or href is None:
            continue

        href = urljoin(initial_url, href)

        parsed_href = urlparse(href)

        # Remove GET parameters, URL fragments, etc.
        href = f"{parsed_href.scheme}://{parsed_href.netloc}{parsed_href.path}"

        if not _internal_validation(href, internal_urls, initial_url):
            continue

        new_urls_set.add(href)


        with lock:
            # get shared memory list, as a set()
            internal_urls_set = set(internal_urls[:])

            # add new url
            internal_urls_set.add(href)

            # store in shared memory the set() as a list()
            internal_urls[:] = internal_urls_set

    return new_urls_set


def _internal_validation(href: str, internal_urls: ListProxy, initial_url: str) -> bool:
    """Make commom validations to decide if a url is valid or not.
    Example:
        -   It the URL is not within the same initial url domain, we should
            return False, to avoid traversing domains.

    Args:
        href (str):
                    The url used on validations.
        internal_urls (ListProxy)
                     A shared memory listing to use in validations.
        initial_url (string):
                    The initial url used to crawl.
    Returns:
        bool: True if all checks pass, False otherwise.
    """
    if not is_valid_link(href):
        return False

    # Is External link?
    if str(urlparse(initial_url).netloc) not in href:
        return False

    if href in internal_urls:
        return False

    return True
